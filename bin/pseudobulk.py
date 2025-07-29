#! /usr/bin/env python

import sys
import pandas as pd

celltype = sys.argv[1]
pseudobulk_summary = sys.argv[2]
unfiltered_outpath = sys.argv[3]
filtered_outpath = sys.argv[4]
gene_expr_threshold = float(sys.argv[5]) / 100  # The gene must be expressed in at least that fraction of individuals
ind_cell_threshold = int(sys.argv[6])  # The individual must have at least this many cells in this celltype
pseudobulk_cell_threshold = int(sys.argv[7])  # The pseudobulk must have at least this many cells to be saved
countmtxs = sys.argv[8:]

def pseudobulk(celltype, countmtx_fnames):
    dfs = [pd.read_csv(countmtx_fname, sep='\t') for countmtx_fname in countmtx_fnames]
    df = pd.concat(dfs, ignore_index=True, axis=0)

    print(f'Pseudobulking {celltype} of {df["n_cells"].sum()} cells and {df.shape[1] - 2} genes.')  # - 2 because of the individual and n_cells columns
    df = df.groupby('individual').sum()
    n_cells = df['n_cells'].copy()
    df.drop(columns='n_cells', inplace=True)
    df = df.div(n_cells, axis=0)  # Divide by the number of cells to get the average expression per cell for each individual
   
    return df, n_cells

def clean_gene_ids(df):
    # Remove PAR genes and warn if they contain any counts
    par_genes = df.columns[df.columns.str.contains('_PAR_Y')]
    if par_genes.size > 0:
        par_counts = df[par_genes].sum().sum()
        if par_counts > 0:
            print(f'WARN: _PAR_Y genes are removed from the pseudobulk but they contain {par_counts} counts.')
        df = df.loc[:, ~df.columns.isin(par_genes)]

    # Remove any suffixes from gene IDs
    df.columns = df.columns.str.extract(r'^(ENSG\d+)', expand=False)

    # If the gene IDs are unique, we're done
    if df.columns.is_unique:
        return df
    
    # Otherwise, average their expression
    duplicated_genes = df.columns[df.columns.duplicated()].unique()
    print(f'After removing suffixes, these gene IDs became duplicated and their expression was averaged:\n{duplicated_genes}')
    df = df.groupby(axis=1, level=0).mean()

    return df
    
pseudobulk_df, n_cells = pseudobulk(celltype, countmtxs)
metadata = {
    'celltype': [celltype], 
    'n_cells_before_ind_filter': [n_cells.sum()], 
    'n_cells_after_ind_filter': [], 
    'n_inds_before_ind_filter': [pseudobulk_df.shape[0]], 
    'n_inds_after_ind_filter': [], 
    'n_genes_before_expr_filter': [pseudobulk_df.shape[1]], 
    'n_genes_after_expr_filter': []
}
print(f'Pseudobulk of {celltype} done with {metadata["n_cells_before_ind_filter"][0]} cells. Contains {metadata["n_inds_before_ind_filter"][0]} individuals and {metadata["n_genes_before_expr_filter"][0]} genes.')

pseudobulk_df = clean_gene_ids(pseudobulk_df)
unfiltered_pseudobulk = pseudobulk_df.copy()

def filter_individuals_two_layers(df, n_cells, abundancy_threshold, strict_ind_filter, lenient_ind_filter):
    # Calculate the average number of cells per individual in this celltype.
    # If this celltype is abundant, i.e. the average number of cells per individual is greater than the abundancy threshold, 
    # we apply the strict individual filter. Otherwise, we apply the lenient individual filter. 
    # The idea is that in abundant celltypes, we can afford to be more strict with the individual filter but 
    # in rare celltypes, we benefit from including more individuals so the filter is more lenient.
    print('\nFiltering out individuals with too few cells in this celltype.')
    avg_cells_per_ind = n_cells.mean()
    print(f'Average number of cells per individual: {avg_cells_per_ind:.2f}')

    ind_filter = strict_ind_filter if avg_cells_per_ind > abundancy_threshold else lenient_ind_filter
    print(f'Applying the {"strict" if ind_filter == strict_ind_filter else "lenient"} individual filter (individual must have >= {ind_filter} cells).')

    # Filter out individuals who have too few cells in this celltype
    ind_has_enough_cells = n_cells >= ind_filter
    df = df[ind_has_enough_cells]

    return df, n_cells[ind_has_enough_cells].sum()

def filter_individuals_simple(df, n_cells, ind_cell_threshold):
    # Filter out individuals who have too few cells in this celltype
    print('\nFiltering out individuals with too few cells in this celltype.')
    ind_has_enough_cells = n_cells >= ind_cell_threshold
    df = df[ind_has_enough_cells]

    return df, n_cells[ind_has_enough_cells].sum()

# Remove individuals with too few cells in this celltype
#abundancy_threshold = 30
#strict_ind_filter = 20
#lenient_ind_filter = 10
pseudobulk_df, cells_left = filter_individuals_simple(pseudobulk_df, n_cells, ind_cell_threshold)
print(f'Pseudobulk retains {pseudobulk_df.shape[0]} individuals and {cells_left} cells.')

# If the celltype has too few cells left, we don't pseudobulk it
if cells_left < pseudobulk_cell_threshold:
    print(f'Abandoning pseudobulking {celltype} because it has fewer than {pseudobulk_cell_threshold} cells left ({cells_left}) after filtering out individuals.')
    sys.exit()

print(f'Pseudobulk contains enough cells (>= {pseudobulk_cell_threshold}) to save the pseudobulk.')
unfiltered_pseudobulk.to_csv(unfiltered_outpath, sep='\t', index=True)
print(f'Unfiltered pseudobulk saved to {unfiltered_outpath}')

# Filter out genes with too low expression
print(f'\nFiltering out genes expressed in < {gene_expr_threshold:%} of individuals).')
pseudobulk_df = pseudobulk_df.loc[:, pseudobulk_df.gt(0).mean(axis=0) >= gene_expr_threshold]
print(f'Pseudobulk retains {pseudobulk_df.shape[1]} genes.')

metadata['n_cells_after_ind_filter'].append(cells_left)
metadata['n_inds_after_ind_filter'].append(pseudobulk_df.shape[0])
metadata['n_genes_after_expr_filter'].append(pseudobulk_df.shape[1])
pd.DataFrame(metadata).to_csv(pseudobulk_summary, sep='\t', index=False)

pseudobulk_df.to_csv(filtered_outpath, sep='\t', index=True)
print(f'Filtered pseudobulk saved to {filtered_outpath}')

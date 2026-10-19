#! /usr/bin/env python

import sys
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt

countmtx = sc.read_10x_mtx(sys.argv[1], gex_only=True)
cell_meta = pd.read_csv(sys.argv[2], sep='\t', index_col='cell_id', dtype={'cell_id': str})
outpath_raw = sys.argv[3]
outpath_norm = sys.argv[4]
sample_id = sys.argv[5]

n_countmtx_cells = countmtx.n_obs
n_meta_cells = cell_meta.shape[0]

# Save the metadata cells that are not in the raw count matrix
meta_in_countmtx = cell_meta.index.isin(countmtx.obs.index)
if not meta_in_countmtx.any():
    raise ValueError("No metadata cell barcodes match the count matrix!")
pd.Series(cell_meta.index[~meta_in_countmtx]).to_csv('meta_cells_not_in_countmtx.txt', header=False, index=False)
cell_meta = cell_meta[meta_in_countmtx]

# Add the individual and cell type labels to the anndata object
countmtx = countmtx[cell_meta.index]  # Filter the countmtx for cells in the metadata
countmtx.obs[['individual', 'celltype']] = cell_meta[['individual', 'celltype']]  # Add the individual and cell type labels to the countmtx

n_shared_cells = countmtx.n_obs

# Save the raw count matrix
countmtx.write_h5ad(outpath_raw, compression='gzip')

# Normalize the count matrix with ln(counts_per_10k + 1)
sc.pp.normalize_total(countmtx, target_sum=1e4)
sc.pp.log1p(countmtx)

# Save the normalized count matrix as well
countmtx.write_h5ad(outpath_norm, compression='gzip')

# Make a simple barplot of the number of cells in the count matrix and metadata
plt.bar(['Metadata', 'Shared'], [n_meta_cells, n_shared_cells])
plt.ylabel('Barcodes')
plt.title(f'{sample_id}\n{n_countmtx_cells:,} barcodes in pool')
plt.tight_layout()
plt.savefig('shared_barcodes.png')

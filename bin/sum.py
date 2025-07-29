#! /usr/bin/env python

import sys
import anndata as ad

print(f'Reading {sys.argv[1]}.')
countmtx_ad = ad.read_h5ad(sys.argv[1])
print(f'Counted {countmtx_ad.shape[0]} cells and {countmtx_ad.shape[1]} genes.')
outpath = sys.argv[2]

countmtx_ad.var.set_index('gene_ids', inplace=True)  # Use gene IDs as column names going forward

df = countmtx_ad.to_df()
df['individual'] = countmtx_ad.obs['individual']
grouped = df.groupby('individual', sort=False, observed=True)
sums = grouped.sum()
n_cells = grouped.size()
n_cells.name = 'n_cells'
df = sums.merge(n_cells, left_index=True, right_index=True)
print(f'Summed counts for {df.shape[0]} individuals across {df["n_cells"].sum()} cells and {df.shape[1] - 1} genes.')  # -1 for the 'n_cells' column
df.to_csv(outpath, sep='\t')
print(f'Summed DF saved to {outpath}.')

#! /usr/bin/env python

import sys
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt

countmtx = sc.read_10x_mtx(sys.argv[1], gex_only=True)
cell_meta = pd.read_csv(sys.argv[2], sep='\t', index_col=0)
outpath_raw = sys.argv[3]
outpath_norm = sys.argv[4]
sample_id = sys.argv[5]

n_countmtx_cells = countmtx.n_obs
n_meta_cells = cell_meta.shape[0]

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

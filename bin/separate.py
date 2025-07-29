#! /usr/bin/env python

import sys
import anndata as ad

sample_id = sys.argv[1]
adata = ad.read_h5ad(sys.argv[2])
celltypes_outdir = sys.argv[3]

for celltype, df in adata.obs.groupby('celltype', sort=False, observed=True):
    celltype_cells = adata[df.index]
    print(f'{sample_id} {celltype} has {celltype_cells.shape[0]} cells')
    celltype_cells.write_h5ad(f'{celltypes_outdir}/{sample_id}.{celltype}.h5ad', compression='gzip')

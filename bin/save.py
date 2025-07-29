#! /usr/bin/env python

import sys
import pandas as pd

pseudobulk_fname = sys.argv[1]
pseudobulk_outpath = sys.argv[2]

pseudobulk = pd.read_csv(pseudobulk_fname, sep='\t', index_col='individual')

# Transpose matrix to the shape gene x individual
pseudobulk = pseudobulk.T

pseudobulk.columns.name = None
pseudobulk.index.name = 'phenotype_id'

pseudobulk.sort_index(inplace=True)

print(f'Saving pseudobulk to {pseudobulk_outpath}')
print(pseudobulk)

pseudobulk.to_csv(pseudobulk_outpath, sep='\t')

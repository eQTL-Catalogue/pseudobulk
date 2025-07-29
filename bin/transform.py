#! /usr/bin/env python

import sys
import numpy as np
import pandas as pd
import scipy.stats as ss

def rank_to_normal(rank, n, c):
    x = (rank - c) / (n - 2 * c + 1)
    return ss.norm.ppf(x)

def inverse_nt(df):
    # Adapted from https://github.com/edm1/rank-based-INT/blob/master/rank_based_inverse_normal_transformation.py
    rng = np.random.default_rng()

    # Rank the data
    df = df.loc[rng.permutation(df.index)]  # Randomly order the rows so that equal values get a random rank
    ranks = ss.rankdata(df, method='ordinal', axis=0)  # Rank the data
    df = pd.DataFrame(ranks, index=df.index, columns=df.columns)

    # Convert to st norm distr
    df = df.apply(lambda x: rank_to_normal(x, n=df.shape[0], c=3.0/8))

    # Sort by the individual ID so it's nicer
    return df.sort_index()

def p(pseudobulk):
    print(pseudobulk)
    print(f'\nMean:\n{pseudobulk.mean()}')
    print(f'\nVariance:\n{pseudobulk.var()}')

pseudobulk_fname = sys.argv[1]
pseudobulk_outpath = sys.argv[2]

pseudobulk = pd.read_csv(pseudobulk_fname, sep='\t', index_col='individual')

print('\nBefore normalization:')
p(pseudobulk)

pseudobulk = inverse_nt(pseudobulk)

print('\nAfter normalization:')
p(pseudobulk)

pseudobulk.to_csv(pseudobulk_outpath, sep='\t', index=True)

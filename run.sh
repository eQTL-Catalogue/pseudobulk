#!/bin/bash

#SBATCH --job-name=pseudobulk
#SBATCH --partition=amd
#SBATCH --time=1-00:00:00
#SBATCH --mem=4G

nextflow -log logs/.nextflow.log run main.nf -profile tartu_hpc \
    --samples assets/input_examples/samples.tsv \
    --outdir results \
    -resume

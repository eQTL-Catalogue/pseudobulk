# pseudobulk
Nextflow workflow for pseudobulking single-cell count matrices

Prerequisites:
* Nextflow
* Singularity

An example of the nextflow run script is in [`run.sh`](run.sh)

Parameters:
* `--samples` TSV containing the sample IDs and data files (examples: [`assets/input_examples/samples`](assets/input_examples/samples))
* `--GE-threshold` percent of individuals that must express the gene to keep it in the pseudobulk (default: 30)
* `--individual-cell-threshold` minimum number of cells an individual must have to be included in the pseudobulk (default: 15)
* `--pseudobulk-cell-threshold` minimum number of cells a cell type must have to pseudobulk it (default: 2000)
* `--outdir` name of the output directory

Outputs:
* `pseudobulks.[meta/annot]` contains the unfiltered, filtered, and filtered + transformed pseudobulks
* `pseudobulk_summary` contains metadata about the pseudobulks

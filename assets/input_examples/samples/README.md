The workflow can pseudobulk single-cell count matrices where
1) the cell type and donor labels are given in one `.h5ad` file or
2) given a path to a cellranger output directory with a separate TSV file of cell type and donor labels or
3) both. In this case, two sets of pseudobulks are generated - one using the counts and annotations from the annotated `.h5ad` file (outputs written to `pseudobulks.annot`), the other with counts from the cellranger output directory and annotations from the metadata file (outputs written to `pseudobulks.meta`)

## Inputfile columns
* **sample** unique identifier for a single-cell sequencing pool. This column is mandatory.
* **countmtx_annot** `.h5ad` count matrix where the donor and cell type labels are in the *individual* and *celltype* columns of the `.obs` DataFrame (examples: [`assets/input_examples/countmtx_annot`](./countmtx_annot)). This count matrix needs to be normalized.
* **countmtx_raw** path to the output directory of the raw Cell Ranger count matrix. The workflow will normalize this count matrix with `ln(counts_per_10,000 + 1)`. Use with **cell_metadata**.
* **cell_metadata** TSV file with the donor and cell type labels (examples: [`assets/input_examples/cell_meta`](./cell_meta)). Use with **countmtx_raw**.

The columns in the inputfile (parameter `--samples`) determine which configuration is run. The inputfile must always contain **sample**. If the inputfile contains **countmtx_annot**, the workflow pseudobulks the `.h5ad` count matrix using the donor and cell type labels in the file and outputs the results to `pseudobulks.annot`. If the inputfile contains **countmtx_raw** and **cell_metadata**, the workflow pseudobulks the count matrix using the donor and cell type labels in the metadata file and outputs results to `pseudobulks.meta`. If the inputfile contains all columns, the workflow makes two sets of pseudobulks.

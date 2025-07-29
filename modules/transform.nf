process TRANSFORM {
    container "quay.io/peepk/scqc_py:v1.0.0"
    tag "$celltype"
    
    input:
    tuple val(celltype), val(fname_prefix), path(pseudobulk)

    script:
    outpath_prefix = "${fname_prefix}.transformed"
    outpath = "${outpath_prefix}.tsv"
    """
    transform.py $pseudobulk $outpath
    """

    output:
    tuple val(celltype), val(outpath_prefix), path(outpath), emit: transformed_pseudobulk
}

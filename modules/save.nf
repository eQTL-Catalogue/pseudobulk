process SAVE {
    container "quay.io/peepk/scqc_py:v1.0.0"
    publishDir "$outdir/$celltype", mode: "copy"
    tag "$celltype"
    
    input:
    tuple val(celltype), val(fname_prefix), path(pseudobulk, stageAs: "input_pseudobulk")
    val(outdir)

    script:
    outpath = "${fname_prefix}.tsv"
    """
    save.py $pseudobulk $outpath
    """

    output:
    path outpath
}

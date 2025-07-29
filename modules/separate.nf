process SEPARATE {
    container "quay.io/peepk/scqc_py:v1.0.0"
    tag "${sample_id}"
    
    input:
    tuple val(sample_id), path(countmtx)

    script:
    celltypes_outdir = sample_id
    """
    mkdir $celltypes_outdir
    separate.py $sample_id $countmtx $celltypes_outdir
    """

    output:
    path("${celltypes_outdir}/*.h5ad"), emit: celltype_countmtxs
}

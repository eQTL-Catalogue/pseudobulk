process SUM {
    container "quay.io/peepk/scqc_py:v1.0.0"
    tag "$f_prefix"
    label "process_low"
    
    input:
    path(countmtx)

    script:
    f_prefix = countmtx.getFileName().toString()[0..<-5]  // Remove the '.h5ad' extension
    outpath = "${f_prefix}.sum.tsv"
    """
    sum.py $countmtx $outpath
    """

    output:
    tuple val(f_prefix), path(outpath), emit: countmtx
}

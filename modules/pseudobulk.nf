process PSEUDOBULK {
    container "quay.io/peepk/scqc_py:v1.0.0"
    tag "$celltype"
    
    input:
    tuple val(celltype), path(countmtxs)
    val pseudobulk_summary

    script:
    unfiltered_prefix = "${celltype}.unfiltered"
    unfiltered_outpath = "${unfiltered_prefix}.tsv"
    filtered_prefix = "${celltype}.filtered"
    filtered_outpath = "${filtered_prefix}.tsv"
    """
    pseudobulk.py $celltype $pseudobulk_summary $unfiltered_outpath $filtered_outpath $params.GEThreshold $params.individualCellThreshold $params.pseudobulkCellThreshold $countmtxs
    """

    output:
    tuple val(celltype), val(unfiltered_prefix), path(unfiltered_outpath), emit: unfiltered_pseudobulk, optional: true
    tuple val(celltype), val(filtered_prefix), path(filtered_outpath), emit: filtered_pseudobulk, optional: true
    path(pseudobulk_summary), emit: pseudobulk_summary, optional: true
}

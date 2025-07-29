process LABEL {
    container "quay.io/peepk/scqc_py:v1.0.0"
    publishDir "$params.outdir/add_meta_labels/${sample_id}", mode: 'copy'
    tag "${sample_id}"
    label "process_low"
    
    input:
    tuple val(sample_id), path(countmtx), path(cell_meta)

    script:
    labelled_countmtx_raw = "countmtx_w_labels.${sample_id}.h5ad"
    labelled_countmtx_norm = "countmtx_w_labels.${sample_id}.norm.h5ad"
    """
    label.py $countmtx $cell_meta $labelled_countmtx_raw $labelled_countmtx_norm $sample_id
    """

    output:
    tuple val(sample_id), path(labelled_countmtx_norm), emit: countmtx_ch
    path(labelled_countmtx_raw)
    path("*.png")
}

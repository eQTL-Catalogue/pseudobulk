include { SUM } from "$projectDir/modules/sum"
include { PSEUDOBULK } from "$projectDir/modules/pseudobulk"

workflow AGGREGATE_WF {
    take:
    countmtxs_ch
    label_type_ch

    main:
    //countmtxs_ch.view()

    summed_countmtxs_ch = SUM(countmtxs_ch).countmtx

    // Remove the sample_id prefix from the id and group by celltype
    celltype_countmtxs_ch = summed_countmtxs_ch.map{ it -> [
        it[0].substring(it[0].indexOf('.') + 1), 
        it[1]
    ]}.groupTuple()
    //celltype_countmtxs_ch.view()

    pseudobulk_summary = "pseudobulk_summary.${label_type_ch}.tsv"
    PSEUDOBULK(celltype_countmtxs_ch, pseudobulk_summary)
    PSEUDOBULK.out.pseudobulk_summary.collectFile(
        name: pseudobulk_summary,
        keepHeader: true, 
        skip: 1, 
        sort: true, 
        storeDir: "${params.outdir}/pseudobulk_summary"
    )

    emit:
    unfiltered_pseudobulks = PSEUDOBULK.out.unfiltered_pseudobulk
    filtered_pseudobulks = PSEUDOBULK.out.filtered_pseudobulk
    /**/
}

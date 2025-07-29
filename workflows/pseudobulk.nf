include { ANNOTATED } from "$projectDir/subworkflows/annotated"
include { METADATA } from "$projectDir/subworkflows/metadata"

workflow PSEUDOBULK {
    main:
    // Decide whether to pseudobulk with the annotated labels or the metadata labels or both
    // based on the samplesheet's columns.

    // Get the header of the samplesheet
    samplesheet_columns = new File(params.samples).withReader { r -> 
        while ((line = r.readLine()) != null) {
            break
        }
        return line.split("\t")
    }
    n_samplesheet_columns = samplesheet_columns.size()
    
    // If the samplesheet has no metadata columns, pseudobulk the annotated mtx only.
    if (n_samplesheet_columns == 2) {
        samples_ch = Channel.fromPath(params.samples, checkIfExists: true)
            .splitCsv(header: true, sep: "\t", strip: true)
            .map { row -> [row.sample, row.countmtx_annot] }

        println("No cell metadata was given in the samplesheet. Pseudobulking with the annotated labels only.")
        ANNOTATED(samples_ch)
    }
    
    // If there is a raw countmtx and a cell metadata column, pseudobulk with metadata labels only.
    else if (n_samplesheet_columns == 3) {
        samples_ch = Channel.fromPath(params.samples, checkIfExists: true)
            .splitCsv(header: true, sep: "\t", strip: true)
            .map { row -> [row.sample, row.countmtx_raw, row.cell_metadata] }
        
        println("Pseudobulking with metadata labels only.")
        METADATA(samples_ch)
    }

    // If there is an annotated countmtx, a raw countmtx, and a cell metadata column, pseudobulk with both.
    else if (n_samplesheet_columns == 4) {
        samples_ch = Channel.fromPath(params.samples, checkIfExists: true)
            .splitCsv(header: true, sep: "\t", strip: true)
            .map { row -> [row.sample, row.countmtx_annot, row.countmtx_raw, row.cell_metadata] }

        println("Pseudobulking with both annotated and metadata labels.")
        ANNOTATED(samples_ch.map{ it -> it[0..1] })
        METADATA(samples_ch.map{ it -> [it[0]] + it[2..-1] })
    }
    
    else {
        error "The samplesheet must have 2 - 4 columns!"
    }
    /**/
}

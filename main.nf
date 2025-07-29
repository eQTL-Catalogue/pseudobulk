nextflow.enable.dsl=2

include { PSEUDOBULK } from "$projectDir/workflows/pseudobulk"

workflow {
    // Print the parameters nicely
    println "Mandatory parameters:"
    def defined_params = [
        ["Samplesheet:", params.samples],
        ["Individual cell threshold:", params.individualCellThreshold],
        ["Pseudobulk cell threshold:", params.pseudobulkCellThreshold],
        ["Gene Expression threshold:", params.GEThreshold], 
        ["Output directory:", params.outdir]
    ]
    def left_width = defined_params.collect { it[0].length() }.max() + 4
    defined_params.each { el -> println "${el[0].padRight(left_width)}${el[1]}" }
    
    PSEUDOBULK()
    /**/
}

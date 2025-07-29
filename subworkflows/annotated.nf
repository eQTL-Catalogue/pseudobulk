include { SEPARATE } from "$projectDir/modules/separate"
include { SAVE as SAVE_untransformed; SAVE as SAVE_transformed } from "$projectDir/modules/save"
include { TRANSFORM } from "$projectDir/modules/transform"
include { AGGREGATE_WF } from "$projectDir/subworkflows/aggregate"

workflow ANNOTATED {
    take:
    samples_ch

    main:
    //samples_ch.view()

    // Separate cells by celltype rather than sample
    samples_celltypes_ch = SEPARATE(samples_ch).celltype_countmtxs.flatten()  // Flatten puts all of the files in one single list of files with names <sample>.<celltype>.h5ad
    //samples_celltypes_ch.view()

    label_type = "annot"
    AGGREGATE_WF(samples_celltypes_ch, label_type)
    save_untransformed_input_ch = AGGREGATE_WF.out.unfiltered_pseudobulks.concat(AGGREGATE_WF.out.filtered_pseudobulks)
    //save_untransformed_input_ch.view()

    finished_pseudobulks_outdir = "$params.outdir/pseudobulks.$label_type"
    SAVE_untransformed(save_untransformed_input_ch, finished_pseudobulks_outdir)

    TRANSFORM(AGGREGATE_WF.out.filtered_pseudobulks)
    save_transformed_input_ch = TRANSFORM.out.transformed_pseudobulk
    //save_transformed_input_ch.view()

    SAVE_transformed(save_transformed_input_ch, finished_pseudobulks_outdir)
    /**/
}

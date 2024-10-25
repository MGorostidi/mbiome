#!/bin/bash

source initialize_parameters.sh

function createReport_experiment() {
    # arguments:
    # 1) AnalysisName
    # 2) kitPrimer
    # 3) difSequenciations
    # 4) sequencer

    # # Change Here
    # local "$AnalysysName"
    # local "$kitPrimer"
    # local "$difSequenciations"
    # local "$sequencer"
   filename="${1}_experiment_report.txt"

    echo -e "${PURPLE}Creating summary report..."
    echo "This is a summary report of the steps followed in the $1 experiment: 
                            DNA Amplification: $2
                            Sequencer: $4
                            Samples sequenced in different runs: $3

                            Steps explanation:
                            When the sequencer has been Ion Torrent and the 16S Metagenomic Kit has been used for DNA amplification, the exact primer sequences used are unknown.
                            Therefore, a trim-left of 15pb will be performed. On the other hand, when the exact primer sequence is known, these can be removed using the nucleotide sequence.
                            When the sequncer has been Illumina, normally specific primer will be used. In this case either primer sequences can be removed or a trimming of Xpb can be performed, based on the quality graph.

                            For ASV identification, DADA2 is performed. For Ion Torrent experiments, denoise-pyro option is used, as recommended in Qiime2Forum.
                            For Illumina experiments, instead, denoise-paired or denoise-single will be used, based on the sequencing type performed. 
                            The truncating value will be chosen based on samples-demux.qzv quality graph. 

                            If samples sequencing has been performed in different runs, DADA2 is need to be conducted separately, for each sequencing run, and then the DADA2 output files are merged, before Taxonomic classification. 

                            The Taxonomic Classification is carried out using both vsearch and blast classifiers. For 16S classification Green Genes database is used. For ITS, instead, UNITE database." >| "$filename"
}



function stepPerform() {
    # arguments:
    # 1) sequencer
    # 2) kitPrimer
    # 3) difSequenciations

    if [ $1 == "IT" ] && [ $2 == "Kit" ]; then
        
        SELECTED_WORKFLOW="IT_MetagenomicsKit"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Ion Torrent Metagenomics Kit!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 0) MetagenomicsPP Plugin for splitting Vregions ${LIGHTCYAN}(write: PP)${ORANGE}
         # 1) Import splitted demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 2.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 3) Taxonomic Classification; both VSEARCH and SIDLE reconstruction options are included ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # ABUNDANCE TABLES?
         # PICRUST?
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}

    elif [ $1 == "IT" ] && [ $2 == "Primers" ]; then   
        SELECTED_WORKFLOW="IT_Primers"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Ion Torrent Primers!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 1) Import demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Cutadapt for known primer removal ${LIGHTCYAN}(write: Cutadapt)${ORANGE}
         # 3) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 3.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 4) Taxonomic Classification VSEARCH ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # ABUNDANCE TABLES?
         # PICRUST?
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}
    
    elif [ $1 == "IL" ] && [ $2 == "Primers" ]; then   
        SELECTED_WORKFLOW="IL_Primers"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Illumina Primers!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 1) Import demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Cutadapt for known primer removal ${LIGHTCYAN}(write: Cutadapt)${ORANGE}
         # 3) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 3.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 4) Taxonomic Classification VSEARCH ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # ABUNDANCE TABLES?
         # PICRUST?
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}
    fi


    if test ${SELECTED_STEP} == "PP"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_PP_splitVregions
    elif test ${SELECTED_STEP} == "Import"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Import
    elif test ${SELECTED_STEP} == "Cutadapt"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Cutadapt
    elif test ${SELECTED_STEP} == "Dada2"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Dada2
    elif test ${SELECTED_STEP} == "Merge"; then 
        echo "Running ${SELECTED_WORKFLOW}_Dada2_merge"
        bash $DIR/src/${SELECTED_WORKFLOW}_Dada2_merge
    # elif test ${SELECTED_STEP} == "Taxonomy"; then 
    #     bash $DIR/src/${SELECTED_WORKFLOW}_tax_classification
    elif [ $SELECTED_STEP == "Taxonomy" ] && [ $SELECTED_WORKFLOW == "IT_MetagenomicsKit" ]; then   
        echo "Running Taxonomic Classification for Metagenomics Kit"
        bash $DIR/src/${SELECTED_WORKFLOW}_tax_classification
    elif [ $SELECTED_STEP == "Taxonomy" ] && [ $SELECTED_WORKFLOW != "IT_MetagenomicsKit" ]; then   
        echo "Running Taxonomic Classification"
        bash $DIR/src/Tax_Classification_Primers
    fi
}



#!/bin/bash

source ../../initialize_parameters.sh

EXPERIMENT_PATH=$PWD

source ${EXPERIMENT_PATH}/config.env

function stepPerform() {
    # arguments:
    # 1) sequencer
    # 2) kitPrimer
    # 3) difSequenciations

    if [ $SEQUENCER == "IT" ] && [ $AMPLIFICATION == "Kit" ] && [ $SPLIT_BY_REGION == "No" ]; then
        
        SELECTED_WORKFLOW="IT_KitNoSplit"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Ion Torrent Metagenomics Kit with NO splitting of regions!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 1) Import splitted demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 2.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 3) Taxonomic Classification ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # 4) Abundance table analysis ${LIGHTCYAN}(write: Analysis)${ORANGE}
         # 5) Functional Analysis by PICRUST2 ${LIGHTCYAN}(write: Picrust)${ORANGE}
         # 6) Functional Analysis by METNET ${LIGHTCYAN}(write: Metnet)${ORANGE}
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}
    
    elif [ $SEQUENCER == "IT" ] && [ $AMPLIFICATION == "Kit" ] && [ $SPLIT_BY_REGION == "Yes" ]; then
        
        SELECTED_WORKFLOW="IT_MetagenomicsKit"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Ion Torrent Metagenomics Kit!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 0) MetagenomicsPP Plugin for splitting Vregions ${LIGHTCYAN}(write: PP)${ORANGE}
         # 1) Import splitted demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 2.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 3) Taxonomic Classification; both VSEARCH and SIDLE reconstruction options are included ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # 4) Abundance table analysis ${LIGHTCYAN}(write: Analysis)${ORANGE}
         # 5) Functional Analysis by PICRUST2 (Remember that this is not possible for Sidle output) ${LIGHTCYAN}(write: Picrust)${ORANGE}
         # 6) Functional Analysis by METNET ${LIGHTCYAN}(write: Metnet)${ORANGE}
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}

    elif [ $SEQUENCER == "IT" ] && [ $AMPLIFICATION == "Primers" ]; then   
        SELECTED_WORKFLOW="IT_Primers"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Ion Torrent Primers!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 1) Import demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Cutadapt for known primer removal ${LIGHTCYAN}(write: Cutadapt)${ORANGE}
         # 3) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 3.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 4) Taxonomic Classification VSEARCH ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # 5) Abundance table analysis ${LIGHTCYAN}(write: Analysis)${ORANGE}
         # 6) Functional Analysis by PICRUST2 (Remember that this is not possible for Sidle output) ${LIGHTCYAN}(write: Picrust)${ORANGE}
         # 7) Functional Analysis by METNET ${LIGHTCYAN}(write: Metnet)${ORANGE}
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}
    
    elif [ $SEQUENCER == "IL" ] && [ $AMPLIFICATION == "Primers" ]; then   
        SELECTED_WORKFLOW="IL_Primers"
        
        echo -e "${LIGHTCYAN}The chosen workflow is Illumina Primers!"
        echo -e "${ORANGE}Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
         # 1) Import demultiplexed files to Qiime2 ${LIGHTCYAN}(write: Import)${ORANGE}
         # 2) Cutadapt for known primer removal ${LIGHTCYAN}(write: Cutadapt)${ORANGE}
         # 3) Dada2 for identifying ASVs ${LIGHTCYAN}(write: Dada2)${ORANGE}
         # 3.1) If samples come from different sequencing runs, previous steps are performed by run, so a merging of Dada2 output is needed ${LIGHTCYAN}(write: Merge)${ORANGE}
         # 4) Taxonomic Classification VSEARCH ${LIGHTCYAN}(write: Taxonomy)${ORANGE}
         # 5) Abundance table analysis ${LIGHTCYAN}(write: Analysis)${ORANGE}
         # 6) Functional Analysis by PICRUST2 (Remember that this is not possible for Sidle output) ${LIGHTCYAN}(write: Picrust)${ORANGE}
         # 7) Functional Analysis by METNET ${LIGHTCYAN}(write: Metnet)${ORANGE}
         #Please select the step:${LIGHTCYAN}(Write one of the above names):"
        read stepDecided
        SELECTED_STEP=${stepDecided}
    fi


    if test ${SELECTED_STEP} == "PP"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_PP_splitVRegions
    elif test ${SELECTED_STEP} == "Import"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Import
    elif test ${SELECTED_STEP} == "Cutadapt"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Cutadapt
    elif test ${SELECTED_STEP} == "Dada2"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Dada2
    elif test ${SELECTED_STEP} == "Merge"; then 
        bash $DIR/src/${SELECTED_WORKFLOW}_Dada2_merge
    # elif test ${SELECTED_STEP} == "Taxonomy"; then 
    #     bash $DIR/src/${SELECTED_WORKFLOW}_tax_classification
    elif [ $SELECTED_STEP == "Taxonomy" ] && [ $SELECTED_WORKFLOW == "IT_KitNoSplit" ]; then 
        echo -e "\n${PURPLE}Running Taxonomic Classification for Metagenomics Kit for $SELECTED_WORKFLOW pipeline"
        bash $DIR/src/Tax_Classification
    elif [ $SELECTED_STEP == "Taxonomy" ] && [ $SELECTED_WORKFLOW == "IT_MetagenomicsKit" ]; then   
        echo -e "\n${PURPLE}Running Taxonomic Classification for Metagenomics Kit for $SELECTED_WORKFLOW pipeline"
        bash $DIR/src/${SELECTED_WORKFLOW}_tax_classification
    elif [ $SELECTED_STEP == "Taxonomy" ] && [ $SELECTED_WORKFLOW != "IT_KitNoSplit" ] && [ $SELECTED_WORKFLOW != "IT_MetagenomicsKit" ]; then   
        echo -e "\n${PURPLE}Running Taxonomic Classification for $SELECTED_WORKFLOW pipeline"
        bash $DIR/src/Tax_Classification_Primers
    #elif test ${SELECTED_STEP} == "Analysis"; then
    elif [ $SELECTED_STEP == "Analysis" ] && [ $SELECTED_WORKFLOW == "IT_KitNoSplit" ]; then 
        echo -e "\n${PURPLE}Running Abundance table analysis for $SELECTED_WORKFLOW pipeline"
        bash $DIR/src/AbundanceTable_analysis_Kitnosplit
    elif [ $SELECTED_STEP == "Analysis" ] && [ $SELECTED_WORKFLOW == "IT_MetagenomicsKit" ]; then 
        echo -e "\n${PURPLE}Running Abundance table analysis for $SELECTED_WORKFLOW pipeline"
        bash $DIR/src/AbundanceTable_analysis_MetagenomicsKit
    elif [ $SELECTED_STEP == "Analysis" ] && [ $SELECTED_WORKFLOW != "IT_KitNoSplit" ] && [ $SELECTED_WORKFLOW != "IT_MetagenomicsKit" ]; then   
        echo -e "\n${PURPLE}Running Abundance table analysis for $SELECTED_WORKFLOW pipeline"
        bash $DIR/src/AbundanceTable_analysis
    elif test ${SELECTED_STEP} == "Metnet"; then
        echo -e "\n${PURPLE}Running Metnet Functional analysis.."
        bash $DIR/src/Function_Metnet

    fi
}


# function createReport_experiment() {
#     # arguments:
#     # 1) AnalysisName
#     # 2) kitPrimer
#     # 3) difSequenciations
#     # 4) sequencer

#     # # Change Here
#     # local "$AnalysysName"
#     # local "$kitPrimer"
#     # local "$difSequenciations"
#     # local "$sequencer"
#    filename="${1}_experiment_report.txt"

#     echo -e "${PURPLE}Creating summary report..."
#     echo "This is a summary report of the steps followed in the $1 experiment: 
#                             DNA Amplification: $2
#                             Sequencer: $4
#                             Samples sequenced in different runs: $3

#                             Steps explanation:
#                             When the sequencer has been Ion Torrent and the 16S Metagenomic Kit has been used for DNA amplification, the exact primer sequences used are unknown.
#                             Therefore, a trim-left of 15pb will be performed. On the other hand, when the exact primer sequence is known, these can be removed using the nucleotide sequence.
#                             When the sequncer has been Illumina, normally specific primer will be used. In this case either primer sequences can be removed or a trimming of Xpb can be performed, based on the quality graph.

#                             For ASV identification, DADA2 is performed. For Ion Torrent experiments, denoise-pyro option is used, as recommended in Qiime2Forum.
#                             For Illumina experiments, instead, denoise-paired or denoise-single will be used, based on the sequencing type performed. 
#                             The truncating value will be chosen based on samples-demux.qzv quality graph. 

#                             If samples sequencing has been performed in different runs, DADA2 is need to be conducted separately, for each sequencing run, and then the DADA2 output files are merged, before Taxonomic classification. 

#                             The Taxonomic Classification is carried out using both vsearch and blast classifiers. For 16S classification Green Genes database is used. For ITS, instead, UNITE database." >| "$filename"
# }

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

    echo -e "${PURPLE} Creating summary report..."
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
    # 1) kitPrimer
    # 2) difSequenciations
    # 3) sequencer

    echo -e "${ORANGE} Now everything is ready, please, select which step would you like to perform. Sometimes we will have some steps already done and we would like to start the analysis from an specific step and no from the beginning. So, we now have the chance of select the step:
    # Import
    # Cutadapt
    # Dada2
    # Merge
    # Taxonomy
    # Diversity
    # SplitTables
    # Picrust2
    # AbundanceAnalysis
    # Picrust2results
    #
    #Please select the step:${LIGHTCYAN}(Write one of the above names):"
    read stepDecided
    # local "$kitPrimer"
    # local "$difSequenciations"
    # local "$sequencer"

    if test ${stepDecided} == "Import"; then
        if [ $3 == "IT" ] && [ $1 == "Kit" ] && [ $2 == "No" ]; then
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IT_Import
        elif [ $3 == "IT" ] && [ $1 == "Kit" ] && [ $2 == "Yes" ]; then               
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IT_Import_different_seqRuns
        elif [ $3 == "IT" ] && [ $1 == "Primers" ] && [ $2 == "No" ]; then 
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IT_Import_Primers
        elif [ $3 == "IT" ] && [ $1 == "Primers" ] && [ $2 == "Yes" ]; then 
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IT_Import_Primers_different_seqRuns
        
        elif [ $3 == "IL" ] && [ $1 == "Primers" ] && [ $2 == "No" ]; then 
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IL_Import_Primers
        elif [ $3 == "IL" ] && [ $1 == "Primers" ] && [ $2 == "Yes" ]; then 
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IL_Import_Primers_different_seqRuns
        fi

    elif test ${stepDecided} == "Cutadapt"; then
        if [ $3 == "IT" ] && [ $1 == "Primers" ] && [ $2 == "No" ]; then 
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IT_Cutadapt_Primers
        elif [ $3 == "IT" ] && [ $1 == "Primers" ] && [ $2 == "Yes" ]; then 
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IT_Cutadapt_Primers_different_seqRuns
        
        elif [ $3 == "IL" ] && [ $1 == "Primers" ] && [ $2 == "No" ]; then 
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IL_Cutadapt_Primers
        elif [ $3 == "IL" ] && [ $1 == "Primers" ] && [ $2 == "Yes" ]; then 
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IL_Cutadapt_Primers_different_seqRuns
        fi
        
    elif test ${stepDecided} == "Dada2"; then
        if [ $3 == "IT" ] && [ $1 == "Kit" ] && [ $2 == "No" ]; then
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IT_16Skit_Dada2
        elif [ $3 == "IT" ] && [ $1 == "Kit" ] && [ $2 == "Yes" ]; then               
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IT_16Skit_Dada2_different_seqRuns
        elif [ $3 == "IT" ] && [ $1 == "Primers" ] && [ $2 == "No" ]; then 
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IT_Primers_Dada2
        elif [ $3 == "IT" ] && [ $1 == "Primers" ] && [ $2 == "Yes" ]; then 
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IT_Primers_Dada2_different_seqRuns
        
        elif [ $3 == "IL" ] && [ $1 == "Primers" ] && [ $2 == "No" ]; then 
            #echo -e "${PURPLE} Importing samples..."
            bash $DIR/src/IL_Primers_Dada2
        elif [ $3 == "IL" ] && [ $1 == "Primers" ] && [ $2 == "Yes" ]; then 
            #echo -e "${PURPLE} Importing samples from different sequencing runs..."
            bash $DIR/src/IL_Primers_Dada2_different_seqRuns
        fi      

    elif test ${stepDecided} == "Merge"; then 
        #echo -e "${PURPLE} Merging tables from different sequencing runs amplified with 16SKit..."
        bash $DIR/src/mergeEdit
        
    elif test ${stepDecided} == "Taxonomy"; then 
        #echo -e "${PURPLE} Starting taxonomical classification..."
        bash $DIR/src/TaxonomicClassification

    elif test ${stepDecided} == "Diversity"; then 
        #echo -e "${PURPLE} Starting diversity analysis..."
        bash $DIR/src/Diversity

    elif test ${stepDecided} == "SplitTables"; then 
        #echo -e "${PURPLE} Starting splitting tables step..."
        bash $DIR/src/SplitDada2Tables

    elif test ${stepDecided} == "Picrust2"; then 
        #echo -e "${PURPLE} Starting Picrust2 functional analysis..."
        bash $DIR/src/PICRUSTpipeline

     elif test ${stepDecided} == "AbundanceAnalysis"; then 
        #echo -e "${PURPLE} Starting Abundance table analysis using R..."
        bash $DIR/src/TaxonomicAnalysis_LefSe_RelAbundTables_byR

     elif test ${stepDecided} == "Picrust2results"; then 
        #echo -e "${PURPLE} Starting Picrust2 results analysis..."
        bash $DIR/src/PicrustAnalysis_statistics_byR

    fi
}



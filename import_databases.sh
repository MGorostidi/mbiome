#!/bin/bash

source initialize_parameters.sh

############## MODIFY THE FOLLOWING VARIABLES ###################
GGfolder="gg_13_8_otus"

UNITEdynamicFasta="sh_refs_qiime_ver10_dynamic_s_04.04.2024"
UNITEdynamicTXT="sh_taxonomy_qiime_ver10_dynamic_s_04.04.2024"

UNITEdynamicFasta="sh_refs_qiime_ver8_dynamic_s_all_04.02.2020"
UNITEdynamicTXT="sh_taxonomy_qiime_ver8_dynamic_s_all_04.02.2020"

UNITEdynamicFasta="sh_refs_qiime_ver10_dynamic_04.04.2024"
UNITEdynamicTXT="sh_taxonomy_qiime_ver10_dynamic_04.04.2024"


##################################################################

echo -e "${PURPLE} Activating $QIIME2_ENV_NAME...${WHITE}"
source $DIR_CONDA
conda activate $QIIME2_ENV_NAME


# GREEN GENES DATABASE FOR 16S:
echo -e "${PURPLE} Importing Green Genes database to Qiime2, identity percentage of: $IDENTITY_PERC...${WHITE}"
IDENTITY_PERC=99

# qiime tools import \
#   --input-path  $DIR_DATABASES/GreenGenes_DB/$GGfolder/trees/${IDENTITY_PERC}_otus.tree \
#   --output-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/${IDENTITY_PERC}_otus_rooted-tree.qza \
#   --type 'Phylogeny[Rooted]'

qiime tools import \
--type 'FeatureData[Sequence]' \
--input-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/rep_set/${IDENTITY_PERC}_otus.fasta \
--output-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/${IDENTITY_PERC}_otus_refs.qza

qiime tools import \
--type 'FeatureData[Taxonomy]' \
--input-format HeaderlessTSVTaxonomyFormat \
--input-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/taxonomy/${IDENTITY_PERC}_otu_taxonomy.txt \
--output-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/${IDENTITY_PERC}_otu_taxonomy.qza


# # UNITE DATABASE FOR ITS:
# echo -e "${PURPLE} Importing UNITE database to Qiime2...${WHITE}"
# qiime tools import \
# --type 'FeatureData[Sequence]' \
# --input-path $DIR_DATABASES/UNITE_DB/$UNITEdynamicFasta.fasta \
# --output-path $DIR_DATABASES/UNITE_DB/unite_dyn_refs.qza

# qiime tools import \
# --type 'FeatureData[Taxonomy]' \
# --input-format HeaderlessTSVTaxonomyFormat \
# --input-path $DIR_DATABASES/UNITE_DB/$UNITEdynamicTXT.txt \
# --output-path $DIR_DATABASES/UNITE_DB/unite_dyn_taxa.qza

# qiime feature-classifier fit-classifier-naive-bayes \
# --i-reference-reads $DIR_DATABASES/UNITE_DB/unite_dyn_refs.qza \
# --i-reference-taxonomy $DIR_DATABASES/UNITE_DB/unite_dyn_taxa.qza \
# --o-classifier $DIR_DATABASES/UNITE_DB/unite_classifier.qza







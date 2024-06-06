#!/bin/bash

Purple='\033[0;35m'
White='\033[1;37m'

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

echo -e "${Purple} Activating $QIIME2_ENV_NAME...${White}"
source /home/unidad/miniconda3/etc/profile.d/conda.sh
conda activate $QIIME2_ENV_NAME


# GREEN GENES DATABASE FOR 16S:
echo -e "${Purple} Importing Green Genes database to Qiime2...${White}"

qiime tools import \
  --input-path  $DIR_DATABASES/GreenGenes_DB/$GGfolder/trees/97_otus.tree \
  --output-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/97_otus_rooted-tree.qza \
  --type 'Phylogeny[Rooted]'

qiime tools import \
--type 'FeatureData[Sequence]' \
--input-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/rep_set/97_otus.fasta \
--output-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/97_otus_refs.qza

qiime tools import \
--type 'FeatureData[Taxonomy]' \
--input-format HeaderlessTSVTaxonomyFormat \
--input-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/taxonomy/97_otu_taxonomy.txt \
--output-path $DIR_DATABASES/GreenGenes_DB/$GGfolder/97_otu_taxonomy.qza

# UNITE DATABASE FOR ITS:
echo -e "${Purple} Importing UNITE database to Qiime2...${White}"

qiime tools import \
--type 'FeatureData[Sequence]' \
--input-path $DIR_DATABASES/UNITE_DB/$UNITEdynamicFasta.fasta \
--output-path $DIR_DATABASES/UNITE_DB/unite_dyn_refs.qza

qiime tools import \
--type 'FeatureData[Taxonomy]' \
--input-format HeaderlessTSVTaxonomyFormat \
--input-path $DIR_DATABASES/UNITE_DB/$UNITEdynamicTXT.txt \
--output-path $DIR_DATABASES/UNITE_DB/unite_dyn_taxa.qza

qiime feature-classifier fit-classifier-naive-bayes \
--i-reference-reads $DIR_DATABASES/UNITE_DB/unite_dyn_refs.qza \
--i-reference-taxonomy $DIR_DATABASES/UNITE_DB/unite_dyn_taxa.qza \
--o-classifier $DIR_DATABASES/UNITE_DB/unite_classifier.qza







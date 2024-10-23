#!/bin/bash

source initialize_parameters.sh

# GREEN GENES DATABASE FOR 16S:
echo -e "${PURPLE} Downloading Green Genes database...${WHITE}"
wget -O $DIR_DATABASES/gg_13_8_otus.tar.gz ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz
mkdir -p $DIR_DATABASES/GreenGenes_DB && tar xvzf $DIR_DATABASES/gg_13_8_otus.tar.gz -C $DIR_DATABASES/GreenGenes_DB


# SILVA DATABASE FOR 16S: 
# from: https://docs.qiime2.org/2024.5/data-resources/
# Citation: bioRxiv 2020.10.05.326504; doi: https://doi.org/10.1101/2020.10.05.326504
mkdir -p $DIR_DATABASES/Silva_DB
echo -e "${PURPLE} Downloading Sivla database...${WHITE}"
wget -O $DIR_DATABASES/Silva_DB/silva-138-99-tax.qza https://data.qiime2.org/2024.5/common/silva-138-99-tax.qza
wget -O $DIR_DATABASES/Silva_DB/silva-138-99-seqs.qza https://data.qiime2.org/2024.5/common/silva-138-99-seqs.qza

#UNITE DATABASE FOR ITS:
echo -e "${PURPLE} Downloading Unite database...${WHITE}"
UNITE_DB=$(ls $DIR_DATABASES/sh_qiime_release_*)
UNITE_DB_NAME=$(basename "$UNITE_DB" .tgz)
mkdir -p $DIR_DATABASES/UNITE_DB && tar xvzf $UNITE_DB -C $DIR_DATABASES/UNITE_DB

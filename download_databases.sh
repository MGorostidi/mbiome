#!/bin/bash

source initialize_parameters.sh

# GREEN GENES DATABASE FOR 16S:
echo -e "${PURPLE} Downloading Green Genes database...${WHITE}"
wget -O $DIR_DATABASES/gg_13_8_otus.tar.gz ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz
mkdir -p $DIR_DATABASES/GreenGenes_DB && tar xvzf $DIR_DATABASES/gg_13_8_otus.tar.gz -C $DIR_DATABASES/GreenGenes_DB


#UNITE DATABASE FOR ITS:
echo -e "${PURPLE} Downloading Unite database...${WHITE}"
UNITE_DB=$(ls $DIR_DATABASES/sh_qiime_release_*)
UNITE_DB_NAME=$(basename "$UNITE_DB" .tgz)
mkdir -p $DIR_DATABASES/UNITE_DB && tar xvzf $UNITE_DB -C $DIR_DATABASES/UNITE_DB

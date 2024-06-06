#!/bin/bash


# Intiialize terminal colors: 
LIGHTCYAN='\033[1;36m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
ORANGE="\033[0;33m"
NC='\033[0m' # No Color


# Define folder path to MBIOME project: 
DIR="/home/unidad/Escritorio/MiriamGorostidi/aMICROBIOTA/mbiome"
DIR_CONDA="/home/unidad/miniconda3/etc/profile.d/conda.sh"

if [ ! -d "$DIR/DATABASES" ]; then
    # Create folder if this one does not exist
    mkdir "$DIR/DATABASES"
fi

DIR_DATABASES=$DIR/DATABASES

if [ ! -d "$DIR/EXPERIMENTS" ]; then
    # Create folder if this one does not exist
    mkdir "$DIR/EXPERIMENTS"
    
fi

DIR_EXPERIMENTS=$DIR/EXPERIMENTS

QIIME2_ENV_NAME=qiime2-amplicon-2024.2

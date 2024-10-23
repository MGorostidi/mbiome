#!/bin/bash

# Initialize terminal colors: 
LIGHTCYAN='\033[1;36m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
ORANGE="\033[0;33m"
NC='\033[0m' # No Color


# Identify Mbiome folder: 
if [ -z "$DIR" ]; then
    if [ "$(basename "$PWD")" == "mbiome" ]; then
        export DIR="$PWD"
    else
        echo "Your current folder is not the "mbiome" folder: $PWD. Please, enter the exact path folder where "mbiome" is located:"
        read -r DIR
        while [ ! -d "$DIR" ] || [ "$(basename "$DIR")" != "mbiome" ]; do
            echo -e "Your current folder is not the "mbiome" folder. Please, try it again:"
            read -r DIR
        done
        export DIR
    fi
fi

# Identify Conda folder: 
conda_dir=$(which conda)
conda_dir=${conda_dir//\/bin\/conda}
DIR_CONDA=${conda_dir}/etc/profile.d/conda.sh

QIIME2_ENV_NAME=qiime2-amplicon-2024.2

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

# V Regions to analyze
V_REGIONS=V2,V3,V4,V67,V8,V9

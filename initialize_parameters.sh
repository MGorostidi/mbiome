#!/bin/bash

# Intiialize terminal colors: 
LIGHTCYAN='\033[1;36m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
ORANGE="\033[0;33m"
NC='\033[0m' # No Color


# Identify Mbiome folder: 
DIR="$(pwd)"

if [[ "$DIR" != *"mbiome" ]]; then
    echo "Your current folder is not the "mbiome" folder: $DIR"
    while read -ep "Now, please, enter the exact path folder where "mbiome" is located:" DIR_USER; do
        if [[ "$DIR_USER" != *"mbiome" ]]; then
            echo -e "Your current folder is not the "mbiome" folder"
        else
            echo -e "Perfect! Now you are in the "mbiom" folder!"
            cd ${DIR_USER}
            DIR=$DIR_USER
            break
        fi
    done
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

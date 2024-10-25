#!/bin/bash
Purple='\033[0;35m'
White='\033[1;37m'

# You can follow the Qiime2 Install instructions: https://docs.qiime2.org/2022.8/install/native/#install-qiime-2-within-a-conda-environment

# Make sure Miniconda is installed.
# If not, install it. (Information in: https://docs.anaconda.com/free/miniconda/)

# Update conda: 
conda update conda
# Install wget: 
conda install wget

# Download .yml file and create qiime2 environment:
echo -e "${Purple} Downloading Qiime2 and creating conda environment... ${White}"
#### MODIFY THE .yml Link:
wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.2-py38-linux-conda.yml

conda env create -n qiime2-amplicon-2024.2 --file qiime2-amplicon-2024.2-py38-linux-conda.yml
# remove .yml file
rm qiime2-amplicon-2024.2-py38-linux-conda.yml

#From Picrust2 tutorial: https://github.com/picrust/picrust2/wiki/PICRUSt2-Tutorial-(v2.3.0-beta)
conda create -n picrust2 -c bioconda -c conda-forge picrust2=2.3.0_b



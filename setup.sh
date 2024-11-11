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
conda env create -n qiime2-amplicon-2024.5 --file https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.5-py39-linux-conda.yml

# Download Metagenomics PP plugin by Thermofisher: (already available when cloning Mbiome repository)
# From https://apps.thermofisher.com/apps/spa/#/publiclib/plugins , after loggin in in the Thermofisher account.
# 1) Log in (or Sign in) in Thermofisher.
# 2) Go to https://apps.thermofisher.com/apps/spa/#/publiclib/plugins 
# 3) Search for MetagenomicsPP and download it
# 4) Unzip the downloaded .zip folder
# 5) Move the MetagenomicsPP folder to the mbiome folder. 


# Downloading and Installing Sidle for reconstruction: 
# Tutorial: https://q2-sidle.readthedocs.io/en/latest/database_preparation.html
echo -e "${Purple} Downloading and Installing Sidle for reconstruction... ${White}"
conda activate qiime2-amplicon-2024.5
conda install dask
conda install -c conda-forge -c bioconda -c qiime2 -c defaults xmltodict
# pip install git+https://github.com/bokulich-lab/RESCRIPt.git # IF RESCRIPT IS NOT INSTALLED IN YOUR QIIME2 ENVIRONMENT (Last versions normally include it)
pip install git+https://github.com/jwdebelius/q2-sidle
qiime dev refresh-cache

# Taxonomic analysis:
conda activate qiime2-amplicon-2024.2
pip install adjustText


# Create Picrust2 environment for Picrust2 analysis: 
echo -e "${Purple} Create Picrust2 environment for Picrust2 analysis... ${White}"
#From Picrust2 tutorial: https://github.com/picrust/picrust2/wiki/PICRUSt2-Tutorial-(v2.3.0-beta)
conda create -n picrust2 -c bioconda -c conda-forge picrust2=2.3.0_b

# Install Metnet for functional analysis:
echo -e "${Purple} Install Metnet for functional analysis... ${White}"
#From tutorial: https://github.com/PlanesLab/q2-metnet
conda activate qiime2-amplicon-2024.5
git clone https://github.com/PlanesLab/q2-metnet.git
cd q2-metnet/q2_metnet/
unzip data.zip
rm data.zip
cd ..
python setup.py install
qiime dev refresh-cache
# mbiome

## MBIOME: A Comprehensive Amplicon Sequencing Analysis Workflow for everyone

Mbiome is a user-friendly workflow designed to streamline the complete analysis of amplicon sequencing data using QIIME2. This workflow is tailored for both 16S (bacterial) and ITS (fungal) amplicon sequences and supports data from Ion Torrent and Illumina platforms.

### Simplified and Interactive:
The workflow is designed to be interactive, guiding users through the process with a series of simple questions about their sample processing. This approach eliminates the need for programming knowledge, making advanced bioinformatics accessible to everyone.

### Versatile and Comprehensive: 
Whether you are working with 16S or ITS amplicon sequences, our workflow has you covered. It is built to handle diverse datasets, ensuring robust and reliable results across different sequencing technologies.

### Fully Automated:
Once you provide the necessary input, the workflow takes care of the rest. It performs all steps of the analysis automatically, from initial processing of raw FASTQ files to detailed downstream analyses.

### Cross-Platform Compatibility:
Our workflow is compatible with FASTQ files generated from both Ion Torrent and Illumina sequencing platforms, ensuring flexibility and broad applicability in various research contexts.

## Workflow diagram and steps: 

!!! ESTOOOOO OTRO DIAAA !!!

## Getting Started

To get started, clone this repository and follow the instructions in the README to install the required dependencies. Then, simply run the workflow and answer the prompted questions to initiate the analysis of your amplicon sequencing data.

### Clone repository: 
1. Clone the repository in a folder: 
```shell
git clone https://github.com/MGorostidi/mbiome.git
```
2. Move to the folder where the repository has been created: 
```
cd mbiome
```

### Installing: 
<!-- 
Mbiome includes a setup.sh file in order to install qiime2 and all the necessary packages and plugins. It installs Qiime2 Amplicon distribution for Linux (Check the link for more information: https://docs.qiime2.org/2024.5/install/native/#install-qiime-2-within-a-conda-environment). If you are working with another operating system, you can change the code line in setup.sh so the right qiime2 distribution is installed. -->

1. Make sure Miniconda is installed in your computer (follow instructions in https://docs.anaconda.com/free/miniconda/)
<!-- 2. Run setup.py file: 
```shell
bash setup.sh
``` -->

2. Update conda:
```shell
conda update conda
```
3. Install wget:
```shell
conda install wget
```
4. Create Qiime2 environment:  
```shell
conda env create -f environment.yml
```

<!-- ```shell
conda env create -n qiime2-amplicon-2024.2 --file="https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.2-py38-linux-conda.yml"
``` 
```shell
wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.2-py38-linux-conda.yml
conda env create -n qiime2-amplicon-2024.2 --file qiime2-amplicon-2024.2-py38-linux-conda.yml
rm qiime2-amplicon-2024.2-py38-linux-conda.yml
```-->
5. Downloading MetagenomicsPP plugin by Thermofisher: 
MetagenomicsPP will be included in mbiome, but if you don't see a folder inside Mbiome, called MetagenomicsPP, you should install it:
```shell
# From https://apps.thermofisher.com/apps/spa/#/publiclib/plugins , after loggin in in the Thermofisher account.
# 1) Log in (or Sign in) in Thermofisher.
# 2) Go to https://apps.thermofisher.com/apps/spa/#/publiclib/plugins 
# 3) Search for MetagenomicsPP and download it
# 4) Unzip the downloaded .zip folder
# 5) Move the MetagenomicsPP folder to the mbiome folder. 
```

6. Downloading and Installing Sidle for reconstruction: 
```shell
# Downloading Sidle and installing Sidle: 
# Tutorial: https://q2-sidle.readthedocs.io/en/latest/database_preparation.html
# Activate your qiime2 environment: 
conda activate qiime2-amplicon-2024.2
conda install dask
conda install -c conda-forge -c bioconda -c qiime2 -c defaults xmltodict
# pip install git+https://github.com/bokulich-lab/RESCRIPt.git # IF RESCRIPT IS NOT INSTALLED IN YOUR QIIME2 ENVIRONMENT (Last versions normally include it)
pip install git+https://github.com/jwdebelius/q2-sidle
qiime dev refresh-cache
```
<!-- 
6. Create Picrust2 environment for Picrust2 analysis: 
```shell
#From Picrust2 tutorial: https://github.com/picrust/picrust2/wiki/PICRUSt2-Tutorial-(v2.3.0-beta)
conda create -n picrust2 -c bioconda -c conda-forge picrust2=2.3.0_b
```
7. Install Metnet for functional analysis: 
```shell
#From tutorial: https://github.com/PlanesLab/q2-metnet
conda activate qiime2-amplicon-2024.2
git clone https://github.com/PlanesLab/q2-metnet.git
cd q2-metnet/q2_metnet/
unzip data.zip
rm data.zip
cd ..
python setup.py install
qiime dev refresh-cache
``` 
-->

### Initial configuration: 
1. Run initialize_parameter.sh included in created mbiome folder:
<!-- 
Open initialize_parameters.sh and update the necessary variables: 
(1) the path to your mbiome project
(2) path to the conda.sh from Miniconda where it has been installed.
(3) the qiime2 version name that you have already installed
Now run the script. 
-->
```shell
bash initialize_parameters.sh
```

2. Download reference databases: 
- Green Genes DB and SILVA DB will be used for 16S characterization. The databases will be downloaded directly in the prepared .sh file. 
- For ITS characterization instead, UNITE database will be used. This needs to be downloaded prior running download_databases.sh file. 

(1) Download UNITE from: https://doi.plutof.ut.ee/doi/10.15156/BIO/2959336<br>
(2) Move the .tar.gz to DATABASES folder<br>
(3) Once the .tar.gz file is saved, we can run the script: 

```shell
bash download_databases.sh
```
4. Import databases to Qiime2:<br>
(1) Since different versions of the databases can be downloaded, we need to write down the exact names of the files at the beginning of the import_databases.sh script.<br>
You will find the exact lines that you need to modify in the file.<br>
(2) Now we can run the file: 
```shell
bash import_databases.sh
```

## Running the workflow: 
Everything is integrated in an unique script, so you just need to run it and answer the questions that it iteractively asks:
```shell
bash Qiime2PIPELINE_MAIN
```
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

### Installing: 

Qiime2 Docs already has a installing step by step tutorial here: https://docs.qiime2.org/2022.8/install/native/#install-qiime-2-within-a-conda-environment

1. Make sure Miniconda is installed in your computer (follow instructions in https://docs.anaconda.com/free/miniconda/)
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
wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.2-py38-linux-conda.yml
conda env create -n qiime2-amplicon-2024.2 --file qiime2-amplicon-2024.2-py38-linux-conda.yml
rm qiime2-amplicon-2024.2-py38-linux-conda.yml
```
5. Create Picrust2 environment for Picrust2 analysis: 
```shell
#From Picrust2 tutorial: https://github.com/picrust/picrust2/wiki/PICRUSt2-Tutorial-(v2.3.0-beta)
conda create -n picrust2 -c bioconda -c conda-forge picrust2=2.3.0_b
```

### Initial configuration: 
1. Open initialize_parameters.sh and update the necessary variables: 
(1) the path to your mbiome project
(2) path to the conda.sh from Miniconda where it has been installed.
(3) the qiime2 version name that you have already installed
Now run the script. 
```shell
bash initialize_parameters.sh
```

2. Download reference databases: 
- Green Genes DB will be used for 16S characterization. The database will be downloaded directly in the prepared .sh file. 
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
bash Qiime2PIPELINE_MAIN.sh
```
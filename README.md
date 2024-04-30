# mbiome

Summary of the pipeline: 
......


Necessary pre-requisites: 
Having Miniconda installed (follow instructions in https://docs.anaconda.com/free/miniconda/)

Steps: 
1. Installing Qiime2:
The setup.sh script can be run for this aim. It does follow the instructions available in Qiime2 webpage (https://docs.qiime2.org/2022.8/install/native/#install-qiime-2-within-a-conda-environment).
(1) Take a look to the setup.sh script and decide if this is the version of Qiime2 that you want to install (if not, change the link to the yml file and the name of the environment)

```
bash setup.sh
```
2. Open initialize_parameters.sh and update the necessary variables: 
(1) the qiime2 version name that you have already installed 
(2) ..??
Now run the script. 
```
bash initialize_parameters.sh
```

3. Download reference databases: 
- Green Genes DB will be used for 16S characterization. The database will be downloaded directly in the prepared .sh file. 
- For ITS characterization instead, UNITE database will be used. This needs to be downloaded prior running download_databases.sh file. 

(1) Download UNITE from: https://doi.plutof.ut.ee/doi/10.15156/BIO/2959336
(2) Move the .tar.gz to DATABASES folder
(3) Once the .tar.gz file is saved, we can run the script: 

```
bash download_databases.sh
```
4. Import databases to Qiime2:
(1) Since different versions of the databases can be downloaded, we need to write down the exact names of the files at the beginning of the import_databases.sh script. 
You will find the exact lines that you need to modify 



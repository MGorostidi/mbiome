import os
import pandas as pd
import argparse

def writeMetadataFiles(path_to_general_metadata_file,region):

    # Cargar el archivo de metadatos
    metadata = pd.read_csv(path_to_general_metadata_file+'/samples-metadata.tsv', sep='\t')

    # Agregar el sufijo '_VX' a la primera columna
    metadata.iloc[1:, 0] = metadata.iloc[1:, 0] + '_'+region

    # Guardar el archivo modificado
    metadata.to_csv(path_to_general_metadata_file+'/samples-metadata-'+region+'.tsv', sep='\t', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create metadata file by region')
    parser.add_argument('path_to_general_metadata_file', type=str, help='Path to general metadata file')
    parser.add_argument('region', type=str, help='Region name for creating its metadata file')
    
    args = parser.parse_args()
    writeMetadataFiles(args.path_to_general_metadata_file,args.region)
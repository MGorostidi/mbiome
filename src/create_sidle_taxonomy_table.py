import os
import pandas as pd
import argparse

def create_sidle_taxonomy_table(path_to_sidle_folder):

    # read samples-metadata from experiment: 
    path_experiment=path_to_sidle_folder.replace('/sidle','')
    metadata_file=pd.read_csv(path_experiment+'/samples-metadata.tsv', sep='\t')
    metadata_file = metadata_file.drop(index=0).reset_index(drop=True)
    metadata_file.columns.values[0]='sample-id'

    # Find both tsv files: 
    folder_path = path_to_sidle_folder
    files = os.listdir(folder_path)
    tsv_files = [f for f in files if f.endswith('.tsv')]

    # Check if at least two .tsv files were found
    if len(tsv_files) < 2:
        print("Both abundance and taxonomy tsv files need to be in the "+path_to_sidle_folder+" folder. Check what is happening..")
    else:
        # Read the files
        # Let's assume that the taxonomy file contains a column named 'Taxon' (adjust as needed)
        taxonomy_file = None
        abundance_file = None

        for file in tsv_files:
            file_path = os.path.join(path_to_sidle_folder, file)
            
            # Check if the file is 'taxonomy.tsv' (ignore column name checks)
            if 'taxonomy.tsv' in file:
                taxonomy_file = file_path  # This is the taxonomy file

            if 'feature-table.tsv' in file:
                abundance_file = file_path
                

        # Check if both files were found
        if taxonomy_file and abundance_file:
            print(f"Taxonomy file found: {taxonomy_file}")
            print(f"Abundance file found: {abundance_file}")
            
            # Load the files into DataFrames
            taxonomy_df = pd.read_csv(taxonomy_file, sep='\t')
            abundance_df = pd.read_csv(abundance_file, sep='\t', skiprows=1)

            # Rename the first column to match (make sure they have the same name)
            abundance_df.rename(columns={abundance_df.columns[0]: 'Feature ID'}, inplace=True)

            # Merge both DataFrames based on the 'Feature ID' column
            merged_df = pd.merge(abundance_df, taxonomy_df, on='Feature ID', how='left')

            # Remove FeatureID column
            merged_df = merged_df.drop(columns=['Feature ID'])

            # Reorganize so Taxon column is the first one, in order to T df: 
            merged_df = merged_df[['Taxon'] + [col for col in merged_df.columns if col != 'Taxon']]
            merged_df = merged_df.set_index('Taxon').T 
            merged_df = merged_df.reset_index().rename(columns={'index': 'sample-id'})

            merged_df=pd.merge(merged_df, metadata_file, on='sample-id', how='left')

            # Save the merged DataFrame to a new file
            merged_df.to_csv(path_to_sidle_folder + '/sidle_abundance_table.csv', sep=',', index=False)

        else:
            print("Couldn't find both taxonomy and abundance files.")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create sidle abundance table')
    parser.add_argument('path_to_sidle_folder', type=str, help='Path to folder where files are saved')
    
    args = parser.parse_args()

    create_sidle_taxonomy_table(args.path_to_sidle_folder)
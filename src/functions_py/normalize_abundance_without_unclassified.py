import os
import pandas as pd

def normalize_abundance_without_unclassified(microbiome_data, output_dir, clean=True, save_normalized=False):
    """
    Normalizes the microbiome abundance values by the total abundance for each sample,
    excluding columns containing "Unclassified". Optionally, it can sum columns ending with ';__' and ';g__'
    if they share the same preceding taxonomy up to ';f__'.

    Parameters:
    microbiome_data (pd.DataFrame): DataFrame containing microbiome data.
    clean (bool): Whether to sum columns ending with ';__' and ';g__' that share the same preceding taxonomy. Default is True.
    save_normalized (bool): Whether to save the normalized data to a CSV file. Default is False.
    output_dir (str): Directory where the normalized data will be saved if save_normalized is True. Default is 'data/'.
    
    Returns:
    pd.DataFrame: DataFrame containing normalized microbiome data without "Unclassified" columns.
    """
    # Identify columns containing "Unclassified"
    unclassified_columns = [col for col in microbiome_data.columns if 'Unclassified' in col] 

    #if len(unclassified_columns)!=0:

    # Exclude columns containing "Unclassified" from normalization
    data_to_normalize = microbiome_data.drop(unclassified_columns, axis=1)

    # Create taxonomy level unclassified and unassigned categories
    # Function to replace column names based on pattern
    def assigned_unclassified(col_name):
        if ';__;__' in col_name:
            return 'Unclassified'
        return col_name

    # Apply the function to each column name
    data_to_normalize.columns = [assigned_unclassified(col) for col in data_to_normalize.columns]

    # Function to replace column names based on pattern
    def assigned_unassigned(col_name):
        if ';f__;g__' in col_name:
            return 'Unassigned'
        return col_name

    # Apply the function to each column name
    data_to_normalize.columns = [assigned_unassigned(col) for col in data_to_normalize.columns]

    # Sum columns with the same name using transpose
    data_to_normalize = data_to_normalize.T.groupby(level=0).sum().T

    # If clean is True, sum columns that end with ';__' and ';g__'
    if clean:
        # Prepare a dictionary to store summed columns
        column_sums = {}
        
        # Iterate through columns to find those ending with ';__'
        for col in data_to_normalize.columns:
            if col.endswith(';g__'):
                # Create new column name by replacing ';__' with ';g__'
                new_col = col.replace(';g__', ';__')
                
                # Sum columns with the same new column name
                if new_col in column_sums:
                    column_sums[new_col] += data_to_normalize[col]
                else:
                    column_sums[new_col] = data_to_normalize[col]

        # Add columns that do not need cleaning to column_sums
        for col in data_to_normalize.columns:
            if not col.endswith(';g__'):
                if col in column_sums:
                    column_sums[col] += data_to_normalize[col]
                else:
                    column_sums[col] = data_to_normalize[col]

        # Convert dictionary to DataFrame
        data_to_normalize = pd.DataFrame(column_sums)

    # Sum columns with the same name using transpose
    data_to_normalize = data_to_normalize.T.groupby(level=0).sum().T

    # Normalize the remaining microbiome data by the total abundance for each sample
    normalized_data = data_to_normalize.div(data_to_normalize.sum(axis=1), axis=0)

    # If save_normalized is True, save the normalized data to a CSV file
    if save_normalized:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the output file path
        output_file = os.path.join(output_dir, 'normalized_abundance_without_unclassified.csv')
        
        # Save the normalized data to the file
        normalized_data.to_csv(output_file, index=True)
    # else:
    #     print("No columns containing uncl found.")
    #     normalized_data=microbiome_data
    #     # Ensure the output directory exists
    #     os.makedirs(output_dir, exist_ok=True)
        
    #     # Define the output file path
    #     output_file = os.path.join(output_dir, 'normalized_abundance_without_unclassified.csv')
        
    #     # Save the normalized data to the file
    #     normalized_data.to_csv(output_file, index=True)

    return normalized_data

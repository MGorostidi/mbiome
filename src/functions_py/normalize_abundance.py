import os

def normalize_abundance(abundance_matrix, output_dir, save_normalized=False):
    """
    Normalizes the microbiome abundance values by the total abundance for each sample.

    Parameters:
    abundance_matrix (pd.DataFrame): DataFrame containing microbiome data.
    output_dir (str): Directory where the normalized data will be saved if save_normalized is True.
    save_normalized (bool): Whether to save the normalized data to a CSV file. Default is False.

    Returns:
    pd.DataFrame: DataFrame containing normalized microbiome data.
    """
    # Normalize the microbiome data by the total abundance for each sample
    normalized_data = abundance_matrix.div(abundance_matrix.sum(axis=1), axis=0)

    # If save_normalized is True, save the normalized data to a CSV file
    if save_normalized:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the output file path
        output_file = os.path.join(output_dir, 'normalized_abundance_matrix.csv')
        
        # Save the normalized data to the file
        normalized_data.to_csv(output_file, index=True)
    
    return normalized_data

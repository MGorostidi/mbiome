import pandas as pd

def import_abundance_matrix(file_path, metadata_columns):
    """
    Imports a CSV file and separates microbiome data from metadata.

    Parameters:
    file_path (str): The path to the CSV file.
    metadata_columns (int): The number of metadata columns at the end of the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing microbiome data.
    pd.DataFrame: DataFrame containing metadata.
    """
    # Read the CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Separate metadata and microbiome data
    abundance_matrix = df.iloc[:, :-metadata_columns]
    metadata = df.iloc[:, -metadata_columns:]

    return abundance_matrix, metadata
import pandas as pd
import numpy as np
from scipy.stats import linregress

def analyze_longitudinal_data(files, output_prefix='change_normalized_abundance', calculate_change=True):
    """
    Analyze longitudinal data from multiple files. If more than two files are provided, perform linear regression.
    
    Parameters:
        files (list of str): List of file paths to CSV files containing the data.
        output_prefix (str): Prefix for the output CSV file names.
        calculate_change (bool): If True, calculate change between two files. If False, perform linear regression on more than two files.
        
    Returns:
        None: Saves the results to CSV files.
    """
    # Load the data from all files into a list of DataFrames
    data_frames = [pd.read_csv(file, index_col=0) for file in files]

    if calculate_change and len(data_frames) == 2:
        # Calculate change between two files
        df_change = data_frames[1] - data_frames[0]
        df_change.to_csv(f'results/{output_prefix}.csv')
    
    elif len(data_frames) > 2:
        # Perform linear regression on each feature across all files
        df_m = pd.DataFrame(index=data_frames[0].index)
        df_n = pd.DataFrame(index=data_frames[0].index)
        
        # Create a list of time points assuming equal spacing
        x_values = np.arange(len(data_frames))
        
        for column in data_frames[0].columns:
            y_values = [df[column].values for df in data_frames]
            y_values = np.vstack(y_values).T
            
            m_values = []
            n_values = []
            for y in y_values:
                m, n, _, _, _ = linregress(x_values, y)
                m_values.append(m)
                n_values.append(n)
                
            df_m[column] = m_values
            df_n[column] = n_values
            
        df_m.to_csv(f'results/{output_prefix}_m_values.csv')
        df_n.to_csv(f'results/{output_prefix}_n_values.csv')
    else:
        raise ValueError("Please provide exactly two files for change calculation or more than two files for regression.")

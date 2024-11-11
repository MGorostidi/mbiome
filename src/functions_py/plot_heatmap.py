import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage
from matplotlib.colors import LinearSegmentedColormap

def simplify_taxonomy(taxonomy):
    """
    Simplify taxonomy names for better readability in heatmaps.

    Parameters:
    taxonomy (str): Full taxonomy name.

    Returns:
    str: Simplified taxonomy name.
    """
    parts = taxonomy.split(';')
    if parts[-1] == '':
        simplified_name = ''
    elif 'g__' in parts[-1] and parts[-1] == 'g__':
        simplified_name = parts[-2].split('__')[-1] + '*'
    elif '__' in parts[-1] and parts[-1] == '__':
        simplified_name = parts[-2].split('__')[-1]
    elif 'g__' in parts[-1]:
        simplified_name = parts[-2].split('__')[-1] + '-' + parts[-1].split('__')[-1]
    else:
        simplified_name = parts[-1].split('__')[-1]
    
    return simplified_name.rstrip('-')

def plot_significant_heatmap(statistical_df, normalized_signed_abundance_matrix, metadata, output_dir, group_column=None, p_value_threshold=0.05, arctan_threshold=2/np.pi * np.arctan(2)):
    """
    Plot a clustered heatmap for significant features based on statistical results, using log-transformed abundance data.
    Includes a dendrogram for clustering and differentiates samples by metadata groups using color bars.

    Parameters:
    statistical_df (pd.DataFrame): DataFrame containing statistical results.
    normalized_signed_abundance_matrix (pd.DataFrame): DataFrame containing normalized abundance data.
    metadata (pd.DataFrame): DataFrame containing metadata to differentiate samples.
    group_column (str): Metadata column to use for sample differentiation with color labels.
    p_value_threshold (float): Threshold for significance of the p-value.
    arctan_threshold (float): Threshold for significance of the arctan fold change.

    Returns:
    None
    """
    # Align the statistical_df with normalized_signed_abundance_matrix based on 'Feature'
    statistical_df = statistical_df.set_index('Feature')
    common_features = statistical_df.index.intersection(normalized_signed_abundance_matrix.columns)
    
    # Filter for significant features
    significant_features = statistical_df.loc[common_features][(statistical_df['Test p-value'] < p_value_threshold) & 
                                          (abs(statistical_df['Arctan Fold Change']) > arctan_threshold)]
    
    # Retrieve corresponding data from normalized_signed_abundance_matrix
    significant_data = normalized_signed_abundance_matrix[significant_features.index]
    
    # Simplify feature names for columns
    simplified_columns = [simplify_taxonomy(col) for col in significant_data.columns]
    significant_data.columns = simplified_columns
    
    # Apply logarithmic transformation to abundance data (adding a small constant to avoid log(0))
    log_transformed_data = np.log10(significant_data + 1e-6)
    
    # Simplify row names (samples)
    simplified_rows = [simplify_taxonomy(row) for row in log_transformed_data.index]
    log_transformed_data.index = simplified_rows
    
    # Create a color palette for metadata groups
    if group_column:
        unique_groups = metadata[group_column].unique()
        palette = sns.color_palette('husl', len(unique_groups))  # Create distinct colors for each group
        group_lut = dict(zip(unique_groups, palette))  # Map groups to colors
        sample_colors = metadata[group_column].map(group_lut)  # Assign colors to samples based on groups
        col_colors = pd.DataFrame(sample_colors, columns=[group_column])
    else:
        col_colors = None

    # Define a custom colormap ranging from light blue to dark blue
    blue_cmap = LinearSegmentedColormap.from_list('blue_cmap', ['lightblue', 'darkblue'])

    # Calculate linkage for clustering (both rows and columns)
    row_linkage = linkage(log_transformed_data, method='average')
    col_linkage = linkage(log_transformed_data.T, method='average')
    
    # Create the clustered heatmap with dendrograms and color labels for metadata groups
    g = sns.clustermap(log_transformed_data, cmap=blue_cmap, row_linkage=row_linkage, col_linkage=col_linkage, 
                       annot=False, linewidths=0.5, row_colors=col_colors, cbar_kws={'label': 'Log-transformed Abundance'},
                       yticklabels=False)  # Remove y-axis tick labels

    # Improve aesthetics
    #g.fig.suptitle('Clustered Heatmap of Log-Transformed Significant Features', fontsize=16)
    plt.xlabel('Significant Features (Simplified)')
    plt.ylabel('Samples')
    #plt.show()
    file_name = f'Heatmap_significant_taxas_Plot.png'
    plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
    plt.close()
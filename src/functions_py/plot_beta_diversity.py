import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import MDS
from scipy.spatial.distance import pdist, squareform
import warnings

def calculate_beta_diversity(df, metric='braycurtis'):
    """
    Calculate a beta diversity matrix for the samples.

    Parameters:
    df (pd.DataFrame): DataFrame containing microbiome data.
    metric (str): The distance metric to use. Common options are 'braycurtis', 'jaccard', etc.

    Returns:
    pd.DataFrame: DataFrame containing the beta diversity distance matrix.
    """
    distance_matrix = pdist(df, metric=metric)
    return pd.DataFrame(squareform(distance_matrix), index=df.index, columns=df.index)

def plot_beta_diversity(normalized_microbiome_data, metadata, output_dir, group='sample-type', metric='braycurtis', palette='pastel'):
    """
    Plot the beta diversity of samples using PCoA.

    Parameters:
    normalized_microbiome_data (pd.DataFrame): DataFrame containing normalized microbiome data.
    metadata (pd.DataFrame): DataFrame containing metadata.
    group (str): Name of the column in metadata that specifies group.
    metric (str): The distance metric to use for beta diversity calculation.
    palette (str): Name of the palette for color mapping.

    Returns:
    None
    """
    # Ensure normalized_microbiome_data and metadata are DataFrames
    if not isinstance(normalized_microbiome_data, pd.DataFrame):
        raise ValueError("normalized_microbiome_data must be a pandas DataFrame")
    
    if not isinstance(metadata, pd.DataFrame):
        raise ValueError("metadata must be a pandas DataFrame")

    # Calculate beta diversity
    beta_diversity_matrix = calculate_beta_diversity(normalized_microbiome_data, metric=metric)

    # Perform PCoA (using MDS as a proxy)
    for i in ['euclidean','precomputed']:
        warnings.filterwarnings("ignore", message="The MDS API has changed")
        mds = MDS(n_components=2, dissimilarity=i, random_state=42)
        pcoa_results = mds.fit_transform(beta_diversity_matrix)
        pcoa_df = pd.DataFrame(pcoa_results, columns=['PC1', 'PC2'], index=beta_diversity_matrix.index)
    
        # Combine PCoA results with metadata
        combined_data = metadata.copy()
        combined_data = combined_data.join(pcoa_df)

        # Plot the PCoA results
        plt.figure(figsize=(6,4))
        sns.scatterplot(x='PC1', y='PC2', hue=group, data=combined_data, palette=palette)
        plt.xlabel('PCo1')
        plt.ylabel('PCo2')
        plt.title(f'PCoA of '+i+' Beta Diversity ('+metric+')')
        plt.legend(title=group, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        #plt.show()
        file_name = f'PCoA_of_'+i+'_Beta_Diversity_'+metric+'.png'
        plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
        plt.close()

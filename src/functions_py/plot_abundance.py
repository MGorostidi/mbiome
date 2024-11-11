import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_abundance(normalized_microbiome_data, metadata, output_dir, group='sample-type', taxonomy_level='Taxonomy', top_n=25, palette='pastel'):
    """
    Plot the abundance of phyla for different groups as a stacked bar plot. 
    If there are more than 25 phyla, plot only the top 25 most abundant ones.

    Parameters:
    normalized_microbiome_data (pd.DataFrame): DataFrame containing normalized microbiome data.
    metadata (pd.DataFrame): DataFrame containing metadata.
    group (str): Name of the column in metadata that specifies group.
    top_n (int): Number of top abundant phyla to plot if there are more than this number.
    palette (str): Name of the seaborn palette for color mapping.

    Returns:
    None
    """
    # Ensure normalized_microbiome_data and metadata are DataFrames
    if not isinstance(normalized_microbiome_data, pd.DataFrame):
        raise ValueError("normalized_microbiome_data must be a pandas DataFrame")
    
    if not isinstance(metadata, pd.DataFrame):
        raise ValueError("metadata must be a pandas DataFrame")

    # Merge microbiome data with metadata
    merged_data = normalized_microbiome_data.merge(metadata[[group]], left_index=True, right_index=True)

    # Calculate mean abundance for each phylum in each group
    mean_abundance = merged_data.groupby(group).mean()

    # If there are more than `top_n` phyla, select the top `top_n` most abundant ones
    if mean_abundance.shape[1] > top_n:
        top_abundances = mean_abundance.mean().sort_values(ascending=False).head(top_n).index
        mean_abundance = mean_abundance[top_abundances]
        others = mean_abundance.sum(axis=1) - mean_abundance.sum(axis=1).loc[mean_abundance.sum(axis=1).index]
        mean_abundance['Others'] = others
        top = str(top_n)
    else:
        top = ''

    # Normalize by converting to percentages
    mean_abundance_percent = mean_abundance.div(mean_abundance.sum(axis=1), axis=0) * 100

    # Create a color palette from seaborn
    color_palette = sns.color_palette(palette, n_colors=mean_abundance_percent.shape[1])

    def simplify_taxonomy(taxonomy):
        parts = taxonomy.split(';')
        # If taxonomy ends with an empty part, return an empty string
        if parts[-1] == '':
            simplified_name = ''
        # If the genus is not assigned (`g__` at the end but no name), use the family name
        elif 'g__' in parts[-1] and parts[-1] == 'g__':
            simplified_name = parts[-2].split('__')[-1] + '*'
        # If the genus is not classified (`__` at the end), use the family name
        elif '__' in parts[-1] and parts[-1] == '__':
            simplified_name = parts[-2].split('__')[-1] 
        # If the genus is assigned, concatenate family and genus
        elif 'g__' in parts[-1]:
            simplified_name = parts[-2].split('__')[-1] + '-' + parts[-1].split('__')[-1]
        else:
            simplified_name = parts[-1].split('__')[-1]
        
        # Remove any trailing hyphens
        return simplified_name.rstrip('-')

    simplified_columns = [simplify_taxonomy(col) for col in mean_abundance_percent.columns]

    # Plot stacked bar plot
    ax = mean_abundance_percent.plot(kind='bar', stacked=True, figsize=(14, 7), color=color_palette)
    plt.xlabel(group.capitalize())
    plt.ylabel('Percentage (%)')
    plt.title(f'{taxonomy_level} Abundance by {group.capitalize()}')
    plt.legend(simplified_columns, title=taxonomy_level + ' ' + top + ' taxonomies', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    #plt.show()
    file_name = f'{taxonomy_level}_Abundance_by_{group.capitalize()}.png'
    plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
    plt.close()

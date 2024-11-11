import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from adjustText import adjust_text

def simplify_taxonomy(taxonomy):
    """
    Simplifies the taxonomy string by extracting the most relevant part, 
    typically the genus or family name. If the genus is unclassified ('g__'), 
    it appends an asterisk (*) to the family name.

    Parameters:
    taxonomy (str): The full taxonomy string.

    Returns:
    str: The simplified taxonomy name.
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

def plot_volcano(results_df, output_dir,  p_value_threshold=0.05, logfc_threshold=2):
    """
    Plots a volcano plot using log fold change and -log10 p-values. Significant points 
    are highlighted in red (upregulated) or blue (downregulated), while others are gray.
    Vertical and horizontal lines are added to denote the p-value and logFC thresholds.

    Parameters:
    results_df (pd.DataFrame): DataFrame containing the results with columns 'Test p-value' 
                               and 'Log Fold Change'.
    p_value_threshold (float, optional): Threshold for significance based on p-value. Default is 0.05.
    logfc_threshold (float, optional): Threshold for significance based on log fold change. Default is 2.
    """
    results_df['-log10(p-value)'] = -np.log10(results_df['Test p-value'])

    def color_point(row):
        if row['Test p-value'] < p_value_threshold:
            if row['Log Fold Change'] > logfc_threshold:
                return 'red'
            elif row['Log Fold Change'] < -logfc_threshold:
                return 'blue'
        return 'gray'
    
    results_df['Color'] = results_df.apply(color_point, axis=1)

    plt.figure(figsize=(6, 4))
    
    # Plot all points with appropriate colors
    sns.scatterplot(x='Log Fold Change', y='-log10(p-value)', data=results_df, 
                    hue='Color', palette={'gray': 'gray', 'blue': 'blue', 'red': 'red'}, 
                    alpha=0.7, legend=None)
    
    # Add horizontal and vertical lines for thresholds
    plt.axhline(-np.log10(p_value_threshold), color='black', linestyle='--', lw=1)
    plt.axvline(logfc_threshold, color='black', linestyle='--', lw=1)
    plt.axvline(-logfc_threshold, color='black', linestyle='--', lw=1)
    
    # Add labels and title
    plt.xlabel('Log Fold Change')
    plt.ylabel('-log10(p-value)')
    
    # Annotate significant points with simplified taxonomy names
    significant_points = results_df[results_df['Color'] != 'gray']
    texts = []
    for _, row in significant_points.iterrows():
        texts.append(plt.text(x=row['Log Fold Change'], y=row['-log10(p-value)'],
                              s=simplify_taxonomy(row['Feature']),
                              fontsize=8, color=row['Color'],
                              ha='center', va='bottom',
                              bbox=dict(facecolor='white', alpha=0.5, edgecolor='none')))
    
    # Adjust text to avoid overlap without using arrows
    adjust_text(texts, 
                only_move={'points': 'x', 'texts': 'y'}, 
                force_text=0.5, 
                expand_text=(1.1, 1.1))

    #plt.show()
    file_name = f'Volcano_Plot.png'
    plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
    plt.close()

def plot_arctanvolcano(results_df, output_dir, p_value_threshold=0.05, logfc_threshold=2):
    """
    Plots a volcano plot using arctan-transformed fold change and -log10 p-values. 
    Significant points are highlighted in red or blue based on the arctan threshold, 
    while others are gray. Vertical and horizontal lines are added to denote the p-value 
    and arctan fold change thresholds.

    Parameters:
    results_df (pd.DataFrame): DataFrame containing the results with columns 'Test p-value' 
                               and 'Arctan Fold Change'.
    p_value_threshold (float, optional): Threshold for significance based on p-value. Default is 0.05.
    arctan_threshold (float, optional): Threshold for significance based on arctan fold change. Default is derived from arctan(2).
    """
    results_df['-log10(p-value)'] = -np.log10(results_df['Test p-value'])

    # Calcule arctan_treshold
    arctan_threshold=2/np.pi * np.arctan(logfc_threshold+1)

    def color_point(row):
        if row['Test p-value'] < p_value_threshold:
            if row['Arctan Fold Change'] > arctan_threshold:
                return 'red'
            elif row['Arctan Fold Change'] < -arctan_threshold:
                return 'blue'
        return 'gray'
    
    results_df['Color'] = results_df.apply(color_point, axis=1)

    plt.figure(figsize=(6,4))
    
    # Plot all points with appropriate colors
    sns.scatterplot(x='Arctan Fold Change', y='-log10(p-value)', data=results_df, 
                    hue='Color', palette={'gray': 'gray', 'blue': 'blue', 'red': 'red'}, 
                    alpha=0.7, legend=None)
    
    # Add horizontal and vertical lines for thresholds
    plt.axhline(-np.log10(p_value_threshold), color='black', linestyle='--', lw=1)
    plt.axvline(arctan_threshold, color='black', linestyle='--', lw=1)
    plt.axvline(-arctan_threshold, color='black', linestyle='--', lw=1)
    
    # Add labels and title
    plt.xlabel('Arctan Fold Change')
    plt.ylabel('-log10(p-value)')
    
    # Annotate significant points with simplified taxonomy names
    significant_points = results_df[results_df['Color'] != 'gray']
    texts = []
    for _, row in significant_points.iterrows():
        texts.append(plt.text(x=row['Arctan Fold Change'], y=row['-log10(p-value)'],
                              s=simplify_taxonomy(row['Feature']),
                              fontsize=8, color=row['Color'],
                              ha='center', va='bottom',
                              bbox=dict(facecolor='white', alpha=0.5, edgecolor='none')))
    
    # Adjust text to avoid overlap without using arrows
    adjust_text(texts, 
                only_move={'points': 'x', 'texts': 'y'}, 
                force_text=0.5, 
                expand_text=(1.1, 1.1))

    plt.tight_layout()
    #plt.show()
    file_name = f'Arctan_FC_Volcano_Plot.png'
    plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
    plt.close()

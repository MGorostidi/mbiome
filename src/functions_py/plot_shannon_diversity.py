import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np
from functions_py.stats import statistics
from functions_py.stats_miri import get_statistics_table


def calculate_shannon_diversity(df):
    """
    Calculate Shannon diversity index for each sample.

    Parameters:
    df (pd.DataFrame): DataFrame containing microbiome data.

    Returns:
    pd.Series: Series containing Shannon diversity index for each sample.
    """
    def shannon_entropy(row):
        proportions = row[row > 0] / row.sum()
        return -sum(proportions * np.log(proportions))

    return df.apply(shannon_entropy, axis=1)

def plot_shannon_diversity(normalized_microbiome_data, metadata, output_dir, group='sample-type', palette='pastel'):
    """
    Plot the Shannon diversity index for each sample divided by groups.
    Additionally, perform a normality test and a statistical test to compare Shannon diversity across groups.

    Parameters:
    normalized_microbiome_data (pd.DataFrame): DataFrame containing normalized microbiome data.
    metadata (pd.DataFrame): DataFrame containing metadata.
    group (str): Name of the column in metadata that specifies group.
    palette (str): Name of the palette for color mapping.

    Returns:
    None
    """
    # Ensure normalized_microbiome_data and metadata are DataFrames
    if not isinstance(normalized_microbiome_data, pd.DataFrame):
        raise ValueError("normalized_microbiome_data must be a pandas DataFrame")
    
    if not isinstance(metadata, pd.DataFrame):
        raise ValueError("metadata must be a pandas DataFrame")

    # Calculate Shannon diversity for each sample
    shannon_diversity = calculate_shannon_diversity(normalized_microbiome_data)
    
    # Combine Shannon diversity with metadata
    combined_data = metadata.copy()
    combined_data['Shannon Diversity'] = shannon_diversity

    # Plot the boxplot
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=group, y='Shannon Diversity', hue=group, data=combined_data, palette=palette, order=sorted(combined_data[group].unique())) #, legend=False)
    plt.legend()
    plt.xlabel(group.capitalize())
    plt.ylabel('Shannon Diversity Index')
    plt.title(f'Shannon Diversity across {group}s')
    plt.tight_layout()
    #plt.show()
    file_name = f'Shannon_Diversity_{group}s.png'
    plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
    plt.close()

    # Perform all statistical tests
    results = statistics(combined_data, group, variable='Shannon Diversity')
    
    if results!=None:
        # Print normality test results
        print("\nNormality Test Results (Shapiro-Wilk Test):")
        for grp, (stat, p_value) in results['normality_results'].items():
            print(f"{grp}: W-stat={stat:.4f}, p-value={p_value:.4f}")
        
        # Print statistical test results
        test_results = results['statistical_test']
        test_name = test_results['test_name']
        stat = test_results['statistic']
        p_value = test_results['p_value']
        fdr_adjusted_p_value = test_results['fdr_adjusted_p_value']
        print(f"\nStatistical Test Results ({test_name}):")
        print(f"{test_name} statistic={stat:.4f}, p-value={p_value:.4f}")
        print(f"FDR-adjusted p-value={fdr_adjusted_p_value:.4f}")

        # Convert 'results' to DataFrame and save:
        results_df = pd.DataFrame.from_dict(results)
        output_file = os.path.join(output_dir, f'ShannonDiversity_across_{group}s_statistics_results.csv')
        results_df.to_csv(output_file, index=False)

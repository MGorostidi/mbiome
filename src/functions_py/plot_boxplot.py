import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
from functions_py.stats import statistics
from functions_py.stats_miri import get_statistics_table


def simplify_taxonomy(taxonomy):
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

def plot_significant_boxplots(statistical_df, normalized_signed_abundance_matrix, metadata, output_dir, group='sample-type', p_value_threshold=0.05, arctan_threshold=2/np.pi * np.arctan(2), palette='pastel'):
    """
    Plot boxplots for significant features differentiated by metadata group.

    Parameters:
    statistical_df (pd.DataFrame): DataFrame containing statistical results.
    normalized_signed_abundance_matrix (pd.DataFrame): DataFrame containing normalized abundance data.
    metadata (pd.DataFrame): DataFrame containing metadata.
    group (str): Name of the column in metadata that specifies the group.
    p_value_threshold (float): Threshold for significance of the p-value.
    arctan_threshold (float): Threshold for significance of the arctan fold change.

    Returns:
    None
    """
    # Align the statistical_df with normalized_signed_abundance_matrix on 'Feature'
    statistical_df = statistical_df.set_index('Feature')
    common_features = statistical_df.index.intersection(normalized_signed_abundance_matrix.columns)
    
    # Filter for significant features
    significant_features = statistical_df.loc[common_features][(statistical_df['Test p-value'] < p_value_threshold) & 
                                          (abs(statistical_df['Arctan Fold Change']) > arctan_threshold)]
    
    for feature in significant_features.index:
        # Extract data for the specific feature
        feature_data = normalized_signed_abundance_matrix[feature]
        
        # Combine feature data with metadata
        combined_data = metadata.copy()
        combined_data['Feature Data'] = feature_data.values
        
        # Plot boxplot
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=group, y='Feature Data', data=combined_data, palette=palette)
        plt.title(f'Boxplot for {simplify_taxonomy(feature)}')
        plt.xlabel(group)
        plt.ylabel('Abundance')
       #plt.show()
        file_name = f'Boxplot_{simplify_taxonomy(feature)}.png'
        plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
        plt.close()

        # # Perform all statistical tests
        # results = statistics(combined_data, group, variable='Feature Data')
        
        # # Print normality test results
        # print("\nNormality Test Results (Shapiro-Wilk Test):")
        # for grp, (stat, p_value) in results['normality_results'].items():
        #     print(f"{grp}: W-stat={stat:.4f}, p-value={p_value:.4f}")
        
        # # Print statistical test results
        # test_results = results['statistical_test']
        # test_name = test_results['test_name']
        # stat = test_results['statistic']
        # p_value = test_results['p_value']
        # fdr_adjusted_p_value = test_results['fdr_adjusted_p_value']
        # print(f"\nStatistical Test Results ({test_name}):")
        # print(f"{test_name} statistic={stat:.4f}, p-value={p_value:.4f}")
        # print(f"FDR-adjusted p-value={fdr_adjusted_p_value:.4f}")

        results = get_statistics_table(combined_data, group)

        output_file = os.path.join(output_dir, f'Taxa_statistics_results.csv')
        results.to_csv(output_file, index=False)
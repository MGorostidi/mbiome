import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functions_py.stats import statistics

def get_sum_columns(dataframe, substring):
    """
    Sum the columns in a dataframe based on a substring.

    Parameters:
    dataframe (pd.DataFrame): DataFrame containing the data.
    substring (str): Substring to match columns.

    Returns:
    pd.Series: Series with summed values of matched columns for each row.
    """
    columns = [col for col in dataframe.columns if substring.lower() in col.lower()]
    return dataframe[columns].sum(axis=1)

def calculate_ratio(dataframe, var1, var2):
    """
    Calculate the ratio of two sets of variables.

    Parameters:
    dataframe (pd.DataFrame): DataFrame containing the data.
    var1 (str): First variable.
    var2 (str): Second variable.

    Returns:
    pd.Series: Series with the calculated ratio.
    """
    summed_var1 = get_sum_columns(dataframe, var1)
    summed_var2 = get_sum_columns(dataframe, var2)
    return summed_var1 / (summed_var2 + 1e-10)  # Adding a small constant to avoid division by zero

def plot_ratio(normalized_microbiome_data, metadata, var1, var2, group='sample-type', palette='pastel'):
    """
    Plot the ratio of two sets of variables as a boxplot and compute statistics.

    Parameters:
    normalized_microbiome_data (pd.DataFrame): DataFrame containing normalized microbiome data.
    metadata (pd.DataFrame): DataFrame containing metadata.
    var1 (str): First variable.
    var2 (str): Second variable.
    group (str): Name of the column in metadata that specifies group.
    palette (str): Seaborn palette name for color mapping.

    Returns:
    None
    """
    # Confirm that the taxonomies are the exact ones, they don't have any extra prefix or sufix
    var1_column = '__' + var1 + ';'
    var2_column = '__' + var2 + ';'

    # Calculate the ratio
    ratio = calculate_ratio(normalized_microbiome_data, var1_column, var2_column)

    # Combine ratio with metadata
    combined_data = metadata.copy()
    combined_data['Ratio'] = ratio

    # Ensure the group variable is a categorical variable for grouping
    if combined_data[group].dtype != 'object':
        combined_data[group] = combined_data[group].astype('category')

    # Plot the ratio
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=group, y='Ratio', data=combined_data, palette=palette, order=sorted(combined_data[group].unique()))
    plt.xlabel(group.capitalize())
    plt.ylabel('Ratio of ' + var1+ ' to ' + var2)
    plt.title('Ratio of ' + var1 + ' to ' + var2 + ' across ' + group + 's')
    plt.tight_layout()
    plt.show()

    # Perform all statistical tests
    results = statistics(combined_data, group, variable='Ratio')

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
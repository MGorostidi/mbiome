import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from functions_py.stats import statistics
from functions_py.stats_miri import get_statistics_table


def plot_unassigned_values(normalized_microbiome_data, metadata, output_dir, substring_to_find='Unassigned', group='sample-type', palette='pastel'):
    """
    Plot values from normalized microbiome data where column names contain a specified substring,
    and visualize the distribution of these values. Compare groups using statistical tests.

    Parameters:
    normalized_microbiome_data (pd.DataFrame): DataFrame containing normalized microbiome data.
    metadata (pd.DataFrame): DataFrame containing metadata.
    substring_to_find (str): Substring to search for in column names.
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

    # Filter for columns containing the specified substring
    columns_with_substring = normalized_microbiome_data.columns[normalized_microbiome_data.columns.str.contains(substring_to_find, case=False)]

    # Ensure there is at least one column with the specified substring
    if len(columns_with_substring) > 0:
        column_to_plot = columns_with_substring[0]  # Selecting the first column with the specified substring

        # Get the values where the specified substring is found
        y_values = normalized_microbiome_data[column_to_plot]

        # Combine y_values with metadata
        combined_data = metadata.copy()
        combined_data[column_to_plot] = y_values

        # Plot the distribution of values
        plt.figure(figsize=(6, 4))
        sns.histplot(y_values, kde=True)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {substring_to_find.lower()} frequency')

        file_name = f'Distribution_{substring_to_find.lower()}_frequency.png'  # Reemplazar espacios por guiones bajos y ajustar el nombre
        #plt.show()
        plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
        plt.close()


        # Plot the boxplot
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=group, y=column_to_plot, data=combined_data, palette=palette, order=sorted(combined_data[group].unique()))
        plt.xlabel(group.capitalize())
        plt.ylabel('Value')
        plt.title(f'{substring_to_find} frequencies across {group}s')
        plt.tight_layout()
        file_name = f'{substring_to_find}_frequencies_across_{group}s.png'  # Reemplazar espacios por guiones bajos y ajustar el nombre
        #plt.show()
        plt.savefig(f'{output_dir}/{file_name}', dpi=300, bbox_inches='tight')
        plt.close()


        # Perform all statistical tests
        results = statistics(combined_data, group, variable=column_to_plot)

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
            print(f"\nStatistical Test Results ({test_name}):")
            print(f"{test_name} statistic={stat:.4f}, p-value={p_value:.4f}")
            print(f"FDR-adjusted p-value={test_results['fdr_adjusted_p_value']:.4f}")


            # Convert 'results' to DataFrame and save:
            results_df = pd.DataFrame.from_dict(results)
            output_file = os.path.join(output_dir, f'{substring_to_find.lower()}_across_{group}s_statistics_results3.csv')
            results_df.to_csv(output_file, index=False)

    else:
        print(f'No columns containing "{substring_to_find}" found.')

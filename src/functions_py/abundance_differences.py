import os
import pandas as pd
import numpy as np
from functions_py.stats import statistics
from statsmodels.stats.multitest import multipletests

def analyze_abundance_differences(normalized_signed_abundance_matrix, metadata, output_dir, group, group_one=None, group_two=None):
    """
    Analyze the differences in abundance between groups for each feature (column) in the normalized_signed_abundance_matrix.
    Outputs a DataFrame with columns: feature name, normality p-value, comparison p-value, fold change, log fold change, 
    adjusted fold change, arctan-transformed fold change, and group comparison.

    The results are saved to /results/abundance_comparison.csv.

    Parameters:
    normalized_signed_abundance_matrix (pd.DataFrame): DataFrame with abundance data.
    metadata (pd.DataFrame): DataFrame containing metadata, including the grouping variable.
    group (str): The column name in metadata used to group the samples.
    group_one (str): Name of the group to be considered as "group one". If None, the first group found will be used.
    group_two (str): Name of the group to be considered as "group two". If None, the second group found will be used.

    Returns:
    pd.DataFrame: A DataFrame summarizing the results.
    """
    results = []
    
    # Determine the unique groups in the data
    groups = metadata[group].unique()

    # Check the number of groups
    num_groups = len(groups)

    if num_groups != 1:
        if num_groups == 2:

            # Set default group_one and group_two if not provided
            if group_one is None:
                group_one = groups[0]
            if group_two is None:
                group_two = groups[1]
            
            p_values = []
            for column in normalized_signed_abundance_matrix.columns:
                combined_data = metadata.copy()
                combined_data['Abundance'] = normalized_signed_abundance_matrix[column]
                
                groups = combined_data[[group, 'Abundance']].groupby([group])['Abundance'].apply(list)
                group_counter = combined_data[[group, 'Abundance']].groupby([group]).apply('count')
                if not all(group_counter['Abundance'] > 2):
                    print("There is no enough data for statistical analysis! (Maybe one of the category has < 3 samples? Shapiro normality test requires at least 3 by group)")
                else:

                    # Perform the statistical analysis
                    stats_result = statistics(combined_data, group, variable='Abundance')
                    p_values.append(stats_result['statistical_test']['p_value'])
            
            if p_values:
                _, fdr_adjusted_p_values, _, _ = multipletests(p_values, method='fdr_bh')
                print("FDR adjusted p-values:", fdr_adjusted_p_values)
            else: 
                print("No p-values to correct.")
            # # Apply FDR correction
            # _, fdr_adjusted_p_values, _, _ = multipletests(p_values, method='fdr_bh')

            # Analyze each feature
            for i, column in enumerate(normalized_signed_abundance_matrix.columns):
                combined_data = metadata.copy()
                combined_data['Abundance'] = normalized_signed_abundance_matrix[column]
                
                # Perform the statistical analysis
                stats_result = statistics(combined_data, group, variable='Abundance')
                
                # Log fold change or other statistical comparison
                group1_data = combined_data[combined_data[group] == group_one]['Abundance']
                group2_data = combined_data[combined_data[group] == group_two]['Abundance']
                
                group1_mean = group1_data.mean()
                group2_mean = group2_data.mean()

                # Calculate fold change and log fold change
                fold_change = group1_mean / group2_mean 
                log_fold_change = np.log2(abs(fold_change)) * np.sign(fold_change)
                
                # Calculate adjusted fold change
                if fold_change > 1:
                    adjusted_fold_change = fold_change - 1
                else:
                    adjusted_fold_change = -((1 / fold_change) - 1)
                
                # Calculate arctan transformation
                arctan_fold_change = (2 / np.pi) * np.arctan(adjusted_fold_change)
                
                # Extracting normality p-value and comparison test information
                normality_p_value = min(p for _, (_, p) in stats_result['normality_results'].items())
                test_name = stats_result['statistical_test']['test_name']
                comparison_p_value = stats_result['statistical_test']['p_value']
                fdr_adjusted_p_value = fdr_adjusted_p_values[i]

                # Append the results
                results.append({
                    'Feature': column,
                    'Group Comparison': f'{group_one} vs {group_two}',
                    'Normality p-value': normality_p_value,
                    'Test': test_name,
                    'Test p-value': comparison_p_value,
                    'Test FDR': fdr_adjusted_p_value,
                    'Fold Change': fold_change,
                    'Log Fold Change': log_fold_change,
                    'Adjusted Fold Change': adjusted_fold_change,
                    'Arctan Fold Change': arctan_fold_change
                })
            
            # Convert results to DataFrame
            results_df = pd.DataFrame(results).sort_values(by='Test p-value')

            # Ensure the /results directory exists
            os.makedirs('results', exist_ok=True)
            
            # Save the results to a CSV file
            results_df.to_csv(f'results/abundance_comparison_{group}_{group_one}vs{group_two}.csv', index=False)
        
        else:
            p_values = []
            for column in normalized_signed_abundance_matrix.columns:
                combined_data = metadata.copy()
                combined_data['Abundance'] = normalized_signed_abundance_matrix[column]
                if not all(group_counter['Abundance'] > 2):
                    print("There is no enough data for statistical analysis! (Maybe one of the category has < 3 samples? Shapiro normality test requires at least 3 by group)")
                else:
                    # Perform the statistical analysis
                    stats_result = statistics(combined_data, group, variable='Abundance')
                    p_values.append(stats_result['statistical_test']['p_value'])
            
            print("tsats vacio??")
            print(stats_result)
            print(stats_result.shape)
            # Apply FDR correction
            _, fdr_adjusted_p_values, _, _ = multipletests(p_values, method='fdr_bh')

            # Analyze each feature
            for i, column in enumerate(normalized_signed_abundance_matrix.columns):
                combined_data = metadata.copy()
                combined_data['Abundance'] = normalized_signed_abundance_matrix[column]
                
                # Perform the statistical analysis
                stats_result = statistics(combined_data, group, variable='Abundance')

                # Extracting normality p-value and comparison test information
                normality_p_value = min(p for _, (_, p) in stats_result['normality_results'].items())
                test_name = stats_result['statistical_test']['test_name']
                comparison_p_value = stats_result['statistical_test']['p_value']
                fdr_adjusted_p_value = fdr_adjusted_p_values[i]

                # Append the results
                results.append({
                    'Feature': column,
                    'Group Comparison': group,
                    'Normality p-value': normality_p_value,
                    'Test': test_name,
                    'Test p-value': comparison_p_value,
                    'Test FDR': fdr_adjusted_p_value
                })
            
            # Convert results to DataFrame
            results_df = pd.DataFrame(results).sort_values(by='Test p-value')

            # # Ensure the /results directory exists
            # os.makedirs('results', exist_ok=True)
            
            # # Save the results to a CSV file
            # results_df.to_csv(f'results/abundance_comparison_{group}.csv', index=False)

            output_file = os.path.join(output_dir, f'abundance_comparison_{group}.csv')
            results_df.to_csv(output_file, index=False)

        
        return results_df

import pandas as pd
from scipy.stats import shapiro, kruskal, f_oneway, ttest_ind, mannwhitneyu
from statsmodels.stats.multitest import multipletests

def statistics(combined_data, group, variable):
    """
    Perform a normality test and the appropriate statistical test to compare the richness across groups.
    Additionally, calculate the False Discovery Rate (FDR) for the statistical test p-values.
    
    Parameters:
    combined_data (pd.DataFrame): DataFrame containing combined data (metadata and richness).
    group (str): Name of the column in metadata that specifies group.
    variable (str): Name of the variable to check for normality and compare.

    Returns:
    dict: A dictionary with normality test results, statistical test results, and FDR-adjusted p-values.
    """

    # print("combined_data")
    # print(combined_data)
    
    # #Check if there is enough data for statistical analysis: 
    groups = combined_data[[group, variable]].groupby([group])[variable].apply(list)
    group_counter = combined_data[[group, variable]].groupby([group]).apply('count')

    if not all(group_counter[variable] > 2):
        print("There is no enough data for statistical analysis! (Maybe one of the category has < 3 samples? Shapiro normality test requires at least 3 by group)")
        # return {
        #     'normality_results': {},  # Diccionario vacío
        #     'statistical_test': {
        #         'test_name': "",          # Cadena vacía
        #         'statistic': None,        # None para valores numéricos vacíos
        #         'p_value': None,
        #         'fdr_adjusted_p_value': None
        #     }
        # }

    else:
        print("Performing statistical analysis for "+str(variable)+" variable")
        # Check normality of richness within each group using Shapiro-Wilk test
        normality_results = {}
        for grp in combined_data[group].unique():
            grp_data = combined_data[combined_data[group] == grp][variable]
            stat, p_value = shapiro(grp_data)
            normality_results[grp] = (stat, p_value)
        
        # Check the number of groups
        num_groups = len(combined_data[group].unique())
        
        # Determine if parametric or non-parametric test is needed
        non_normal = any(p < 0.05 for _, p in normality_results.values())
        
        if num_groups == 2:
            # If there are exactly two groups
            if non_normal:
                # Use Mann-Whitney U test (non-parametric)
                groups = [combined_data[combined_data[group] == grp][variable] for grp in combined_data[group].unique()]
                stat, p_value = mannwhitneyu(*groups)
                test_name = "Mann-Whitney U"
            else:
                # Use t-test (parametric)
                groups = [combined_data[combined_data[group] == grp][variable] for grp in combined_data[group].unique()]
                stat, p_value = ttest_ind(*groups)
                test_name = "T-test"
        else:
            # If there are more than two groups
            if non_normal:
                # Use Kruskal-Wallis test (non-parametric)
                groups = [combined_data[combined_data[group] == grp][variable] for grp in combined_data[group].unique()]
                stat, p_value = kruskal(*groups)
                test_name = "Kruskal-Wallis"
            else:
                # Use ANOVA test (parametric)
                groups = [combined_data[combined_data[group] == grp][variable] for grp in combined_data[group].unique()]
                stat, p_value = f_oneway(*groups)
                test_name = "ANOVA"
        
        # FDR calculation
        p_values = [p_value]  # Create a list of p-values
        _, fdr_adjusted_p_values, _, _ = multipletests(p_values, method='fdr_bh')
        
        return {
            'normality_results': normality_results,
            'statistical_test': {
                'test_name': test_name,
                'statistic': stat,
                'p_value': p_value,
                'fdr_adjusted_p_value': fdr_adjusted_p_values[0]  # Access the first element
            }
        }
        # data = []
        # for norm_result in normality_results:
        #     data.append({
        #         'normality_statistic': norm_result[0],  # Primer valor de la tupla
        #         'normality_p_value': norm_result[1],    # Segundo valor de la tupla
        #         'test_name': test_name,
        #         'statistic': stat,
        #         'p_value': p_value,
        #         'fdr_adjusted_p_value': fdr_adjusted_p_values[0]
        #     })
        # return data

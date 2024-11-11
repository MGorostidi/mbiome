# stats.py

import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

def get_variables_statistics_with_dependent_variable(variable_name, dependent_variable, dataframe):

    groups = dataframe[[dependent_variable, variable_name]].groupby([dependent_variable])[variable_name].apply(list)
    group_counter = dataframe[[dependent_variable, variable_name]].groupby([dependent_variable]).apply('count')

    if not all(group_counter[variable_name] > 2):
        TEST_NAME = np.nan
        TEST_PVALUE = np.nan
    else:
        number_of_groups = len(groups)
        all_groups_normal = all(groups.apply(lambda x: stats.shapiro(x)[1]) > 0.05)

        if all_groups_normal and number_of_groups == 2:
            TEST_NAME = 'T-test'
            #TEST_PVALUE = stats.ttest_ind(groups[0], groups[1])[1]
            TEST_PVALUE = stats.ttest_ind(groups[groups.index[0]], groups[groups.index[1]])[1]

        elif all_groups_normal and number_of_groups > 2:
            TEST_NAME = 'One-way ANOVA test'
            TEST_PVALUE = stats.f_oneway(*groups)[1]

        elif not all_groups_normal and number_of_groups == 2:
            TEST_NAME = 'Mann-Whitney test'
            #TEST_PVALUE = stats.mannwhitneyu(groups[0], groups[1])[1]
            TEST_PVALUE = stats.mannwhitneyu(groups[groups.index[0]], groups[groups.index[1]])[1]
            
        else:
            TEST_NAME = 'Kruskal-Wallis H-test'
            TEST_PVALUE = stats.kruskal(*groups)[1]

    GROUP_SIZES = (", ").join(['= N:'.join(i) for i in zip(group_counter.index.astype(str).tolist(), group_counter[variable_name].astype(str))])
    NUM_SAMPLES = str(group_counter[variable_name].sum()) + ' (' + GROUP_SIZES + ')'
    

    return (pd.DataFrame({'variable_name': [variable_name],
                'test_applied': [TEST_NAME],
                'num_samples': [NUM_SAMPLES],
                'test_pvalue': [TEST_PVALUE]}))


def get_statistics_table(dataframe, dependent_variable):

    variables = dataframe.drop([dependent_variable], axis = 1).columns
    df_stats = pd.DataFrame()
    for variable in variables:
        df_stats = pd.concat([df_stats, get_variables_statistics_with_dependent_variable(variable, dependent_variable, dataframe)])

    df_stats = df_stats[df_stats['test_pvalue'].notna()]

    if df_stats.shape[0] > 1 :
            
        # FDR calculation
        _, fdr_adjusted_p_values, _, _ = multipletests(df_stats['test_pvalue'], method='fdr_bh')
        df_stats['test_pvalue_fdr_adjusted']=fdr_adjusted_p_values

    return df_stats
# %% [markdown]
# # mbiome

# %% [markdown]
# ## Import

# %%
import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import argparse

from functions_py.import_abundance_matrix import import_abundance_matrix
from functions_py.normalize_abundance import normalize_abundance
from functions_py.plot_unnasigned_values import plot_unassigned_values
from functions_py.normalize_abundance_without_unclassified import normalize_abundance_without_unclassified
from functions_py.plot_richness import plot_richness
from functions_py.plot_shannon_diversity import calculate_shannon_diversity, plot_shannon_diversity
from functions_py.plot_beta_diversity import calculate_beta_diversity, plot_beta_diversity
from functions_py.plot_abundance import plot_abundance
from functions_py.abundance_differences import analyze_abundance_differences
from functions_py.volcano_plot import plot_volcano
from functions_py.volcano_plot import plot_arctanvolcano
from functions_py.plot_boxplot import plot_significant_boxplots
from functions_py.plot_ratio import plot_ratio
from functions_py.plot_heatmap import plot_significant_heatmap
from functions_py.stats_miri import get_statistics_table

if __name__ == '__main__':

    ######## PREGUNTAR TODOS LOS ATRIBUTOS PARA PODER HACER CON CUALQUIER NIVEL!
    parser = argparse.ArgumentParser(description='Analyze abundance table')
    parser.add_argument('output_dir', type=str, help='Path to the folder where the output figures will be saved')
    parser.add_argument('abundance_matrix_path', type=str, help='Path to the abundance table file in .csv')
    parser.add_argument('num_metadata_columns', type=str, help='Number of how many metadata columns the abundance table contains')
    parser.add_argument('metadata_column_to_analyze', type=str, help='Metadata column to analyze')
    parser.add_argument('taxonomy_level', type=str, help='Taxonomy level to work on. Ex: "Genus"')

    args = parser.parse_args()


    # Read parameters: 
    output_dir=args.output_dir
    abundance_matrix_path=args.abundance_matrix_path
    num_metadata_columns=args.num_metadata_columns
    group_column = args.metadata_column_to_analyze
    tax_level=args.taxonomy_level

    num_metadata_columns_int=num_metadata_columns.strip()
    num_metadata_columns_int=int(num_metadata_columns_int)
    num_metadata_columns_int=num_metadata_columns_int-1

    abundance_matrix, metadata = import_abundance_matrix(abundance_matrix_path, num_metadata_columns_int)

    ### Preprocessing
    # Remove unwanted characters from column names
    abundance_matrix.columns = abundance_matrix.columns.str.replace('[\[\]\|]', '', regex=True) # Check if taxonomies: taxa and taxa2
    # Replace "Unassigned" with "Unclassified" in column names
    abundance_matrix.columns = abundance_matrix.columns.str.replace('Unassigned', 'Unclassified', regex=False) 
    # Replace "k_Bacteria"/"d_Bacteria"/"k_Fungi"with "Unclassified" in column names
    abundance_matrix.columns = abundance_matrix.columns.str.replace('k_Bacteria;__', 'Unclassified;__', regex=False) 
    abundance_matrix.columns = abundance_matrix.columns.str.replace('d_Bacteria;__', 'Unclassified;__', regex=False) 
    abundance_matrix.columns = abundance_matrix.columns.str.replace('k_Fungi;__', 'Unclassified;__', regex=False) 

    ### Same taxonomy merge
    # Sum columns with the same name using transpose
    abundance_matrix = abundance_matrix.T.groupby(level=0).sum().T

    ### Remove taxonomies without at least 5%
    # Calculate the threshold for 5% of the rows
    threshold = 0.05 * len(abundance_matrix)
    # Identify columns that have at least 'threshold' number of non-zero values
    non_zero_counts = (abundance_matrix > 0).sum()
    valid_columns = non_zero_counts[non_zero_counts >= threshold].index
    # Filter the DataFrame to keep only valid columns
    abundance_matrix = abundance_matrix[valid_columns]


    # # MaAsLin2: 
    # import subprocess
    # subprocess.run(['Rscript', 'ruta/al/script.R', abundance_matrix_path, num_metadata_columns_int], check=True)



    ### Quality control
    ### Normalization
    # We normalize the microbiome abundance values by the total abundance for each sample.
    # Normalize data
    print("Normalizing abundance table..")
    normalized_abundance_matrix = normalize_abundance(abundance_matrix, output_dir, save_normalized=True)

    ### Unclassified values
    # We plot the unassigned values for each sample.
    # Assuming metadata and normalized_abundance_matrix are already defined
    # Ensure they are correctly loaded or generated beforehand
    # Define the substring to find in column names
    substring_to_find = 'Unclassified'
 
    # Call the plotting function
    print("Creating Unnasigned plot..")
    plot_unassigned_values(normalized_abundance_matrix, metadata, output_dir, substring_to_find, group_column)

    ### Normalization without unclassified values

    # Afterwards, we will work with the normalized signed abundance table.
    # Normalize data 
    normalized_signed_abundance_matrix = normalize_abundance_without_unclassified(abundance_matrix, output_dir, clean=True, save_normalized=True)

    ### Analysis
    ## Richness
    print("Creating Richness plot..")
    plot_richness(normalized_signed_abundance_matrix, metadata, output_dir, group=group_column, palette='pastel')
    ## Shanon diversity 
    print("Creating Shannon Diversity plot..")
    plot_shannon_diversity(normalized_signed_abundance_matrix, metadata, output_dir, group=group_column, palette='pastel')
    ## Beta Diversity
    print("Creating Beta Diversity plot..")
    plot_beta_diversity(normalized_signed_abundance_matrix, metadata, output_dir, group=group_column, metric='braycurtis', palette='pastel')

    ## Abundance
    print("Plotting abundance barplot..")
    plot_abundance(normalized_signed_abundance_matrix,metadata,output_dir,group=group_column,taxonomy_level=tax_level)
    # abundance analysis
    # Assuming `normalized_signed_abundance_matrix` and `metadata` are your dataframes and `group` is the grouping variable
    #abundance_table = analyze_abundance_differences(normalized_signed_abundance_matrix, metadata, group=group_column, group_one='Untreated', group_two='Rebif44')
    print("Performing statistical analysis in taxonomies by selected group..")
    abundance_table_stats = analyze_abundance_differences(normalized_signed_abundance_matrix, metadata, output_dir, group=group_column)

    if abundance_table_stats!=None:
        print("Plotting Volcano plots..")
        plot_volcano(abundance_table_stats, output_dir)
        plot_arctanvolcano(abundance_table_stats, output_dir)

        # Boxplot graph of significantly different taxonomies: 
        print("Plotting boxplot of significant taxonomies..")
        plot_significant_boxplots(abundance_table_stats, normalized_signed_abundance_matrix, metadata, output_dir)
        # Heatmap
        print("Plotting heatmap graph of significant taxonomies..")
        plot_significant_heatmap(abundance_table_stats, normalized_signed_abundance_matrix, metadata, output_dir, group_column=group_column)








    # ###############33 PENDIENTE!

    # # # Quieres calcular frimicutes/bacteroidetes? SI -_> se lee direcatment el level-2.csv
    # # plot_ratio(normalized_signed_abundance_matrix,metadata, var1='Firmicutes',var2='Bacteroidetes',group='sample-type')


    # # %% [markdown]
    # # ### Longitudinal, darl una vueta
    # # 
    # # En caso de tener dos timepoints, sacar el delta, y calcular el fold change basandonos en la media de los grupos.
    # # 
    # # En caso de tener mas de dos grupos sacar una funcion y comparar el m y n. El m nos diría si el cambio es significativo entre los grupos y la n si el valor original era distinta o no.

    # # %% [markdown]
    # # ### LEFSE /maanslim2 ?




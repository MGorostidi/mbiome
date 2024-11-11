if(!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("Maaslin2")

library(Maaslin2)
library(dplyr)

input_data="/home/unidad/Escritorio/MiriamGorostidi/aMICROBIOTA/mbiome/EXPERIMENTS/IT/sidle/sidle_abundance_table.csv"
num_metadata_cols=
input_metadata="/home/unidad/Escritorio/MiriamGorostidi/aMICROBIOTA/mbiome/EXPERIMENTS/IT/samples-metadata.tsv"

df_input_data = read.table(file = input_data, header = TRUE, sep = "\t",
                            row.names = 1,
                            stringsAsFactors = FALSE)

df_input_metadata = read.table(file = input_metadata, header = TRUE, sep = "\t",
                                row.names = 1,
                                stringsAsFactors = FALSE)


#Filter abundance table so only taxonomies that appear in at least 5% of samples are retained. 
# thres <- ceiling(0.05 * nrow(df_input_data))  # 5% of samples (rounded)
# filtered_df_input_data <- df_input_data %>% select(where(~ sum(. > 0) > thres))
# fit_data = Maaslin2(
#   input_data = filtered_df_input_data, 
#   input_metadata = df_input_metadata, 
#   output = "/home/unidad/Escritorio/MiriamGorostidi/aMICROBIOTA/mbiome/EXPERIMENTS/IT/sidle/maaslin2_output", 
#   fixed_effects = c("sample.type", "sex"))

fit_data = Maaslin2(
  input_data = df_input_data, 
  input_metadata = df_input_metadata, 
  output = "/home/unidad/Escritorio/MiriamGorostidi/aMICROBIOTA/mbiome/EXPERIMENTS/IT/sidle/maaslin2_output", 
  fixed_effects = c("sample.type", "sex"),
  min_prevalence = 0.1,
  min_abundance = 0.0001)




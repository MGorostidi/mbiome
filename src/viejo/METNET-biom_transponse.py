# %%
import os
import pandas as pd

# %%
import sys

current_dir_bash = sys.argv[1]




# %%
#dir='/home/unidad/Escritorio/MiriamGorostidi/aMICROBIOTA/mbiome/EXPERIMENTS/Prueba16S/exported-dada2table'

df = pd.read_csv(f"{current_dir_bash}/exported-dada2table/feature-table.tsv", sep='\t', skiprows=1)
df =df.reset_index(drop=True)
df_transposed = df.transpose()

df_transposed.columns=df_transposed.iloc[0,]

df_transposed = df_transposed.iloc[1:]

df_transposed.to_csv(f"{current_dir_bash}/exported-dada2table/transposed-feature-table.tsv", sep='\t')


# %%




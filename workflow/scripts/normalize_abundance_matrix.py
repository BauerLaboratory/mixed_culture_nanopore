import pandas as pd
import glob,os
from cmath import nan
import math

in_matrix=str(snakemake.input.matrix)
prepool=str(snakemake.params.prepool_name)

df = pd.read_csv(in_matrix, sep="\t", index_col="cell_line")

time_points=list(df.columns)


df = df.drop("sum")
time_points=list(df.columns)
cell_lines=df.index.values.tolist()

df= df.T

for i in cell_lines:
    prepool_value = df.loc[prepool, i]
    df[i] = (df[i] / prepool_value).round(6)

df["sum"]=df.sum(axis=1)
df=df.T

for i in time_points:
    sum_value = df.loc["sum", i]
    df[i] = ((df[i] / sum_value).round(3))*100


df = df.drop("sum")
df=df.T

with open(snakemake.output.tab_out, 'w') as output_f:
    print(df.to_csv(sep="\t", index=True, header=True), file=output_f)
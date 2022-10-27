import pandas as pd
import glob,os

input_files=(snakemake.input)


df_final = pd.DataFrame(columns=["cell_line"])

for i in input_files:
    df=pd.read_table(i, sep="\t")
    df_final= pd.merge(df_final, df, on="cell_line", how="outer")

df_final=df_final.sort_values(by=["cell_line"])
df_final=df_final.set_index("cell_line")
df_final.loc["sum"] = df_final.sum()

with open(snakemake.output[0], 'w') as output_f:
    print(df_final.to_csv(sep="\t", index=True, header=True), file=output_f)
import pandas as pd
import glob,os

input_files=(snakemake.input)


df_final = pd.DataFrame(columns=["QNAME"])

for i in input_files:
    df=pd.read_table(i, sep="\t")
    df_final= pd.merge(df_final, df, on="QNAME", how="outer")
    df_final.drop_duplicates(subset="QNAME", keep="last", inplace=True)

df_final


with open(snakemake.output[0], 'w') as output_f:
    print(df_final.to_csv(sep="\t", index=False, header=True), file=output_f)
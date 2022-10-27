from cmath import nan
import pandas as pd
import numpy as np



mutation_tsv = pd.read_csv(snakemake.input.mutation_tsv, sep="\t", index_col="QNAME") 
cell_lines= pd.read_csv(snakemake.input.cell_lines, sep="\t")
sample_tsv=pd.read_csv(snakemake.input.sample_tsv, sep="\t", index_col="sample_name")

# get time point name
time_point=str(snakemake.params.sample_name)



# make dictionary for mapping names of cell lines to mutations
# sort the mutations
to_rep = {}
for i in cell_lines:
    l=cell_lines[i].dropna().unique().tolist()
    l=list(map(lambda x: x.lower(), l))
    l_sort=sorted(l)
    l_sort="_".join(l_sort)
    to_rep[str(l_sort)] = str(i) 


# remove all valus that are not in the mutation list such as wt
list_mutations=list(mutation_tsv.columns)
for i in list_mutations:
    mutation_tsv[i] = np.where(mutation_tsv[i].isin(list_mutations), mutation_tsv[i], nan)

# sort columns/mutations
mutation_tsv.columns=mutation_tsv.columns.str.lower()
mutation_tsv = mutation_tsv.reindex(sorted(mutation_tsv.columns), axis=1)
# make new column with the mutations
mutation_tsv[time_point] = mutation_tsv[mutation_tsv.columns].apply(lambda x: "_".join(x.dropna().astype(str)),axis=1)
mutation_tsv[time_point] = mutation_tsv[time_point].str.lower()


# map cell lines to mutations. It works best.
mutation_tsv[time_point]=mutation_tsv[time_point].map(to_rep)



# count cell lines
abd=mutation_tsv[time_point].value_counts().to_frame()

# make final dataframe

abd["cell_line"] = abd.index
df_final = abd[["cell_line", time_point]]



with open(snakemake.output[0], 'w') as output_f:
    print(df_final.to_csv(sep="\t", index=False, header=True), file=output_f)
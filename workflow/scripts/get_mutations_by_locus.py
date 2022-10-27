import pandas as pd
import glob,os
from cmath import nan
import math

mpileup=str(snakemake.input.mpileup)
mutation_tsv=str(snakemake.params.mutation_tsv)
sam=str(snakemake.input.sam)
samples_tsv=str(snakemake.params.samples_tsv)
sample_name=str(snakemake.params.sample_name)

locus=int(snakemake.params.locus)
sam_filter_pos_start=int(snakemake.params.cDNA_pos_start)
sam_filter_pos_end=sam_filter_pos_start + 50
amplicon_length=int(snakemake.params.amplicon_length)



##### import tabels
mpileup = open(mpileup, "r").readlines()[0].split("\t")

mutation_tsv = pd.read_csv(mutation_tsv, sep='\t')
mutation_tsv=mutation_tsv.sort_values(by=["pos_cDNA"], ascending=True)
mutation_tsv=mutation_tsv.set_index("pos_cDNA")
mut_name=mutation_tsv.loc[locus]["name"]

sam=pd.read_csv(sam, sep='\t', usecols=range(11), header=None, low_memory=False)
cols = ["QNAME", "FLAG", "RNAME", "POS", "MAPQ", "CIGAR", "RNEXT", "PNEXT", "TLEN", "SEQ", "QUAL"]
sam.columns = cols

samples_tsv = pd.read_csv(samples_tsv, sep='\t')
samples_tsv=samples_tsv.set_index("sample_name")


########## filter sam: position length
# df["FLAG"] == 0               --> mapped to the forward strand
# df["POS"] > 1450  and <1500   --> all reads that starts at the positon
# df["SEQ"].str.len() > 1150    --> reads length more than...

sam=sam.loc[(sam["FLAG"] == 0) & (sam["POS"] > sam_filter_pos_start) & (sam["POS"] < sam_filter_pos_end) & (sam["SEQ"].str.len() > amplicon_length)]


df_final=pd.DataFrame()
df_final=sam[["QNAME"]]



def get_snv(x):
    if x == mutation_tsv.loc[locus]["alt"]:
        return mutation_tsv.loc[locus]["name"]
    elif x != mutation_tsv.loc[locus]["ref"]:
        return "snv"
    return "wt"

#########################
########## snv ##########
#########################
if mutation_tsv.loc[locus]["type"] == "snv":
    df = pd.DataFrame()
    df["QNAME"]=mpileup[7].split(",")
    df["pos_in_read"]=mpileup[6].split(",")
    df["ref"]=mutation_tsv.loc[locus]["ref"]
    df["alt"]=mutation_tsv.loc[locus]["alt"]

    df= pd.merge(sam, df, on='QNAME', how="outer")
    df=df[df['SEQ'].notna()]
    df=df[df['pos_in_read'].notna()]

    df=df.astype(str)
    df["pos_in_read"] = df["pos_in_read"].apply(pd.to_numeric)
    df["alt_read"] = df.apply(lambda x: x["SEQ"][(x["pos_in_read"])-1],axis=1)
    df[mutation_tsv.loc[locus]["name"]] = df["alt_read"].apply(get_snv)

    df=df[["QNAME",mutation_tsv.loc[locus]["name"]]]
    df_final= pd.merge(df_final, df, on='QNAME', how="outer")

#########################
########## del ##########
#########################

elif mutation_tsv.loc[locus]["type"] == "del":
    alt=mutation_tsv.loc[locus]["alt"]
    del_len=str(mutation_tsv.loc[locus]["alt_length"])+"D"
    
    del_len=str(mutation_tsv.loc[locus]["alt_length"])+"D"
    alt=mutation_tsv.loc[locus]["alt"]
    mut_name=mutation_tsv.loc[locus]["name"]


    # get the positions in read at given locus
    df = pd.DataFrame()
    df["QNAME"]=mpileup[7].split(",")
    df["pos_in_read"]=mpileup[6].split(",")
    df["pos_in_read"] = df["pos_in_read"].astype("int")
    # merge sam and mpilup positions by read name
    df= pd.merge(df, sam, on='QNAME', how="outer")

    # get positions when length is in the mutations.tsv
    if (math.isnan(mutation_tsv.loc[locus]["alt_length"])):
        df=df[df['SEQ'].notna()]
    else:
        # get the positions in read at given locus plus minus
        df=df[df['SEQ'].notna()]
        df=df[df['pos_in_read'].notna()]
        df["pos_in_read_start"]=df["pos_in_read"].apply(lambda x: x - 10).astype("int")
        df["pos_in_read_start"]=df["pos_in_read_start"].clip(lower=0).astype("int")
        df["pos_in_read_end"]=df["pos_in_read"].apply(lambda x: x + 10 + int(mutation_tsv.loc[locus]["alt_length"])).astype("int")
        ####################################### Extraction ##################
        df["extracted_seq"] = df.apply(lambda x: x["SEQ"][x["pos_in_read_start"] : x["pos_in_read_end"]],axis=1)


    if (math.isnan(mutation_tsv.loc[locus]["alt_length"])):
        df[mut_name] = df.apply(lambda x: mut_name  if alt in x.SEQ else "wt", axis=1)
    else:
        df[mut_name] = df.apply(lambda x: mut_name  if ((alt in x.extracted_seq)) else "wt", axis=1)

    df_final=df[["QNAME", mut_name]]


#########################
########## ins ##########
#########################
elif mutation_tsv.loc[locus]["type"] == "ins":
    alt=mutation_tsv.loc[locus]["alt"]
    del_ins=str(mutation_tsv.loc[locus]["alt_length"])+"I"

    # get the positions in read at given locus
    df = pd.DataFrame()
    df["QNAME"]=mpileup[7].split(",")
    df["pos_in_read"]=mpileup[6].split(",")
    df["pos_in_read"] = df["pos_in_read"].astype("int")
    # merge sam and mpilup positions by read name
    df= pd.merge(df, sam, on='QNAME', how="outer")


    # get positions when length is in the mutations.tsv
    if (math.isnan(mutation_tsv.loc[locus]["alt_length"])):
        df=df[df['SEQ'].notna()]
    else:
        # get the positions in read at given locus plus minus
        df=df[df['SEQ'].notna()]
        df=df[df['pos_in_read'].notna()]
        df["pos_in_read_start"]=df["pos_in_read"].apply(lambda x: x - len(alt)*2 - 10).astype("int")
        df["pos_in_read_start"]=df["pos_in_read_start"].clip(lower=0).astype("int")
        df["pos_in_read_end"]=df["pos_in_read"].apply(lambda x: x + 10 + len(alt) + int(mutation_tsv.loc[locus]["alt_length"])).astype("int")
        ####################################### Extraction ##################
        df["extracted_seq"] = df.apply(lambda x: x["SEQ"][x["pos_in_read_start"] : x["pos_in_read_end"]],axis=1)

    if (math.isnan(mutation_tsv.loc[locus]["alt_length"])):
        df[mut_name] = df.apply(lambda x: mut_name  if alt in x.SEQ else "wt", axis=1)
    else:
        df[mut_name] = df.apply(lambda x: mut_name  if ((alt in x.extracted_seq)) else "wt", axis=1)

    df_final=df[["QNAME", mut_name]]

    df_final=df[["QNAME", mut_name]]


#########################
########## err ##########
#########################
else: 
    print("Check file: mutations.tsv! Colum type should contains one of this values: snv, ins or del")


with open(snakemake.output.mut_out, 'w') as output_f:
    print(df_final.to_csv(sep="\t", index=False, header=True), file=output_f)
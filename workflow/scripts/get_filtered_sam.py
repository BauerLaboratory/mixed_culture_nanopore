import pandas as pd
import glob,os
from cmath import nan
import math



sam=str(snakemake.input.sam_in)

sam_filter_pos_start=int(snakemake.params.cDNA_pos_start)
sam_filter_pos_end= sam_filter_pos_start + 50
amplicon_length=int(snakemake.params.amplicon_length)
samples_tsv=str(snakemake.params.samples_tsv)
sample_name=str(snakemake.params.sample_name)



##### import tabels

# sometimes EOF error-> solution -> encoding='utf-8', engine='python', error_bad_lines=False
sam=pd.read_csv(sam, sep='\t', usecols=range(11), header=None, encoding='utf-8', engine='python', error_bad_lines=False)
cols = ["QNAME", "FLAG", "RNAME", "POS", "MAPQ", "CIGAR", "RNEXT", "PNEXT", "TLEN", "SEQ", "QUAL"]
sam.columns = cols

samples_tsv = pd.read_csv(samples_tsv, sep='\t')
samples_tsv=samples_tsv.set_index("sample_name")


########## filter sam: position length
# df["FLAG"] == 0               --> mapped to the forward strand
# df["POS"] > 1450  and <1500   --> all reads that starts at the positon
# df["SEQ"].str.len() > 1150    --> reads length more than...


sam=sam.loc[(sam["FLAG"] == 0) & (sam["POS"] > sam_filter_pos_start) & (sam["POS"] < sam_filter_pos_end) & (sam["SEQ"].str.len() > amplicon_length)]



with open(snakemake.output.sam_out, 'w') as output_f:
    print(sam.to_csv(sep="\t", index=False, header=False), file=output_f)
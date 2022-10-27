import glob
from os import path

import pandas as pd
from snakemake.remote import FTP
from snakemake.utils import validate

ftp = FTP.RemoteProvider()




samples_tsv = pd.read_csv(config["samples"], sep="\t", dtype={"sample_name": str, "fastq": str, "barcode": str, "comment": str}).set_index("sample_name", drop=False)
mutations_tsv = pd.read_csv(config["mutations"], sep="\t", dtype={"name": str, "pos_cDNA": str}).set_index("name", drop=False)

SAMPLES=samples_tsv.sample_name.to_list()
LOCUS=mutations_tsv.pos_cDNA.to_list()


def get_fastq(wildcards):
    fastq=[samples_tsv.loc[wildcards.sample]["fastq"]]
    return fastq



def get_barcode(wildcards):
    barcode=[samples_tsv.loc[wildcards.sample]["barcode"]]
    return barcode



def get_final_output():
    final_output = []
    
    final_output=expand(["results/normalize.matrix.tsv","results/bar_plot_abundance.jpg"], sample=SAMPLES, locus=LOCUS)
    
    return final_output
import Bio
from Bio import SeqIO


fq_in=sam=str(snakemake.input.fq_in)

min_read_len=int(snakemake.params.min_read_len)


with open(snakemake.output.fq_out, "w") as output_filtered:
    for record in SeqIO.parse(fq_in, "fastq"):
        if len(record) > min_read_len:
            SeqIO.write(record, output_filtered, "fastq")
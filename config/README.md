`samples.tsv`: provide sample names (time points/names), path to the fastq file and barcode for demultiplexing. When the fastq is already demultiplexed, set in the barcode column only one letter, "A" for example.

`mutations.tsv`: name of the mutation, position in the reference, ref and alt allele, type and length of the alt allele are needed. The `type` column needs to contain the variant type (one of 'snv', 'ins' or 'del'). 

`cell_lines.tsv`: provide cell line names in the first row and in the columns names of the mutations (same names as in the mutations.tsv) respectively. 

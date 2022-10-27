rule demultiplexing:
    input:
        get_fastq,
    output:
        "results/fastq/demultiplex/{sample}.demultiplex.fq"
    params:
        barcode =get_barcode
    log:
        "logs/demultiplexing/{sample}.log"
    shell: 
        "(grep -B1 -A2 {params.barcode} {input} | grep -v \"^--$\" > {output}) 2>{log}"



rule filter_amplicon_length:
    input:
        fq_in="results/fastq/demultiplex/{sample}.demultiplex.fq",
    output:
        fq_out="results/fastq/filtered/{sample}.fq"
    params:
        min_read_len=config["params"]["amplicon_length"]
    conda:
        "../envs/biopython.yaml"
    script:
        "../scripts/filter_read_length_fq.py"
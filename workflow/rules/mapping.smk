rule samtools_index_fa:
    input:
        config["reference"],
    output:
        config["reference"]+".fai",
    log:
        "logs/samtools/index/genome.fai.log",
    params:
        extra="",  # optional params string
    wrapper:
        "v1.10.0/bio/samtools/faidx"



rule minimap2_index:
    input:
        target=config["reference"],
        fai=config["reference"]+".fai",        
    output:
        config["reference"]+".mmi"
    log:
        "logs/minimap2_index/resources/genome.log"
    params:
        extra=""  # optional additional args
    threads: 4
    wrapper:
        "v1.10.0/bio/minimap2/index"



rule minimap2:
    input:
        target=config["reference"]+".mmi",  # can be either genome index or genome fasta
        query="results/fastq/filtered/{sample}.fq",
    output:
        "results/bam_files/{sample}.bam",
    log:
        "logs/minimap2/{sample}.log",
    params:
        extra="-x map-ont",  # optional
        sorting="coordinate",  # optional: Enable sorting. Possible values: 'none', 'queryname' or 'coordinate'
        sort_extra="",  # optional: extra arguments for samtools/picard
    threads: 8
    wrapper:
        "v1.10.0/bio/minimap2/aligner"



rule index_bam:
    input:
        "results/bam_files/{sample}.bam"
    output:
        "results/bam_files/{sample}.bam.bai"
    conda:
        "../envs/samtools.yaml"
    log:
        "logs/samtools/index_bam/{sample}.log"
    shell:
        "(samtools index {input} > {output}) 2> {log}" 



rule samtools_bam_to_sam:
    input:
        "results/bam_files/{sample}.bam"
    output:
        "results/sam_files/{sample}.sam"
    conda:
        "../envs/samtools.yaml"
    log:
        "logs/samtools/filter_reads/{sample}.log"
    shell:
        "(samtools view --no-header {input} > {output}) 2> {log}"



# Filtered sam for igv viewer
rule get_filtered_sam:
    input:
        sam_in="results/sam_files/{sample}.sam",
    output:
        sam_out="results/sam_filtered/{sample}.filtered.sam",
    params:
        amplicon_length=config["params"]["amplicon_length"],
        cDNA_pos_start=config["params"]["cDNA_pos_start"],
        samples_tsv=config["samples"],
        sample_name="{sample}"
    conda:
        "../envs/pandas.yaml"
    script:
        "../scripts/get_filtered_sam.py"
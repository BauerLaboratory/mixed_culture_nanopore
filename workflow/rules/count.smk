rule mpileup:
    input:
        bam="results/bam_files/{sample}.bam",
        bai="results/bam_files/{sample}.bam.bai"
    output:
        expand("results/mpilup/{{sample}}/{{locus}}.tsv")
    conda:
        "../envs/samtools.yaml"
    params:
        locus="1:{locus}-{locus}",
        extras=config["params"]["mpileup_extras"]
    log:
        "logs/samtools/mpileup/{{sample}}_{{locus}}.log"
    shell:
        "(samtools mpileup --output-QNAME -O {params.extras} -r {params.locus} {input.bam} > {output}) 2> {log}" 


ruleorder: mpileup > get_mutations_by_locus 


rule get_mutations_by_locus:
    input:
        mpileup="results/mpilup/{sample}/{locus}.tsv",
        sam="results/sam_filtered/{sample}.filtered.sam",
    output:
        mut_out="results/mut_by_locus/{sample}/{locus}.tsv",
    params:
        mutation_tsv=config["mutations"],
        samples_tsv=config["samples"],
        locus="{locus}",
        amplicon_length=config["params"]["amplicon_length"],
        cDNA_pos_start=config["params"]["cDNA_pos_start"],
        sample_name="{sample}"
    conda:
        "../envs/pandas.yaml"
    script:
        "../scripts/get_mutations_by_locus.py"


rule merge_mutations_by_sample:
    input:
        expand("results/mut_by_locus/{{sample}}/{locus}.tsv", locus=LOCUS),
    output:
        "results/tab_mut/{sample}.tsv"
    conda:
        "../envs/pandas.yaml"
    script:
        "../scripts/merge_mutations_by_sample.py"


rule abundance_matrix_per_time_point:
    input:
        mutation_tsv="results/tab_mut/{sample}.tsv",
        cell_lines=config["cell_lines"],
        sample_tsv=config["samples"],
    output:
        "results/abundance_matrix_per_sample/{sample}_abundance.tsv"
    conda:
        "../envs/pandas.yaml"
    params:
        sample_name="{sample}"
    script:
        "../scripts/abundance_matrix_per_tp.py"


rule merge_abundance_matrix:
    input:
        matrix=expand("results/abundance_matrix_per_sample/{sample}_abundance.tsv", sample=SAMPLES),
    output:
        "results/abundance.matrix.tsv"
    conda:
        "../envs/pandas.yaml"
    script:
        "../scripts/merge_abundance_matrix.py"


rule normalize_abundance_matrix:
    input:
        matrix="results/abundance.matrix.tsv",
    output:
        tab_out="results/normalize.matrix.tsv"
    conda:
        "../envs/pandas.yaml"
    params:
        prepool_name=config["prepool_name"]
    script:
        "../scripts/normalize_abundance_matrix.py"


rule bar_plot_abundance:
    input:
        abundance_matrix="results/normalize.matrix.tsv",
    output:
        plot_out="results/bar_plot_abundance.jpg"
    conda:
        "../envs/pandas.yaml"
    script:
        "../scripts/bar_plot_abundance.py"
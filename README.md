[![Snakemake](https://img.shields.io/badge/snakemake-≥7.12.1-brightgreen.svg)](https://snakemake.github.io)

# Project: "Mixed Culture - Nanopore"

This simple approach estimates the abundance of cell lines with known alternations in a specific gene in a mixed culture experiment. 

The cells are seeded in a dish (pre-pool) and then treated with inhibitors, to simulate cancer therapy for example. 
At pre-pool and certain time points or by agent switches RNA is extracted, amplified by One-Step reverse transcriptase-PCR with barcoded gene specific primers and sequenced with the Nanopore technology.

The long reads are then mapped with [minimap2](https://lh3.github.io/minimap2/minimap2.html) to reference, filtered, assigned to the cell line, counted and normalized to the pre-pool. Afterwards, clonal prevalence plots can be draw with [TimeScape](https://bioconductor.org/packages/release/bioc/vignettes/timescape/inst/doc/timescape_vignette.html). 


## Installation and execution

First, install [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

Next, set up the files in the config directory.

Afterwards, start the Conda environment with installed Snakemake and run first a dry-run (-n or --dry-run flag):

    snakemake --use-conda -n

If the dry-run is fine then run the workflow:

    snakemake --use-conda --cores N

N = number of used cores/threads. For more information about Snakemake see the [documentation](https://snakemake.readthedocs.io/en/stable/).


## Clonal plots
The final table (`normalized.abundance.tsv`) can be used as input file in order to draw clonal plots. 
In the directory clonal_plots an R script can be found. 
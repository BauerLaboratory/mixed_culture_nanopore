import pandas as pd
import matplotlib.pyplot as plt

abundance_matrix=str(snakemake.input.abundance_matrix)


df = pd.read_csv(abundance_matrix, sep="\t", index_col=0)


df.plot(kind="bar", stacked=True)
 
# labels for x & y axis
plt.xlabel("Time points")
plt.ylabel("Relative abundance in %")
 
# title of plot
plt.title("Relative abundance")

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))



plt.savefig(snakemake.output.plot_out, dpi=1000, bbox_inches='tight')
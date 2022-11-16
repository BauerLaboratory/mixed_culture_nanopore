if (!requireNamespace("BiocManager", quietly=TRUE)) install.packages("BiocManager")
if (!requireNamespace("reshape2", quietly=TRUE)) install.packages("reshape2")
if (!requireNamespace("dplyr", quietly=TRUE)) install.packages("dplyr")
if (!requireNamespace("htmlwidgets", quietly=TRUE)) install.packages("htmlwidgets")
if (!requireNamespace("timescape", quietly=TRUE)) BiocManager::install("timescape")


library(timescape)
library(reshape2)
library(dplyr)
library(htmlwidgets)


# example("timescape")


# set working directory
setwd("C:/Users/daw/Desktop/plots")

# pathways
clonal_prev_path="normalized.matrix.tsv"
tree_edges_path="tree_edges.tsv"
clone_colours_path="clone_colours.tsv"
plot_matrix_path="plot_matrix.tsv"



# import and prepare table
clonal_prev = read.table(file = clonal_prev_path, sep = "\t", header = TRUE)
clonal_prev= melt(clonal_prev, id.var = c("X"), variable.name = 'outcomes')
names(clonal_prev) <- c("timepoint", "clone_id","clonal_prev")
clonal_prev[is.na(clonal_prev)] <- 0  # or 0.0001???

tree_edges = read.table(file = tree_edges_path, sep = "\t", header = TRUE)
clone_colours = read.table(file = clone_colours_path, sep = "\t", header = TRUE)

plot_matrix=read.table(file = plot_matrix_path, sep = "\t", header = TRUE)


plot_names=unique(plot_matrix$plot_name)

for (i in plot_names)
{
  print(paste("Draw plot ", i))
  tp=filter(plot_matrix, plot_name %in% i)
  tp=tp$time_points
  df=filter(clonal_prev, timepoint %in% tp)
  file_name=paste(i,".html")
  x_title=paste(i)
  saveWidget(timescape(df, tree_edges, xaxis_title = x_title, clone_colours=clone_colours), file=file_name)
}


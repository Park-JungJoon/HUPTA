BiocManager::install("rhdf5")
library("rhdf5")    # can be installed using Bioconductor
destination_file = "the path to the file" # the path to the file, h5 file from archs4
extracted_expression_file = "file_name.tsv" # gene count table's file name 

setwd("")

# Build meta data of GEO 
samples = h5read(destination_file, "meta/samples/geo_accession")
tissues = h5read(destination_file, "meta/sample/source_name_ch1")
scp = h5read(destination_file, "meta/sample/singlecellprobability")

meta_sample = cbind(samples,tissues,scp)
write.table(meta_sample, file = 'raw_archs4_meta.tsv', row.names = FALSE,quote = FALSE,sep='\t')

# Build Gene information table
genes = h5read(destination_file, "meta/genes/gene_symbol")
ensg =  h5read(destination_file, "meta/genes/ensembl_gene_id")
gene_symbol = h5read(destination_file, "/meta/genes/gene_symbol")

gene_data = cbind(genes,ensg,gene_symbol)
write.table(gene_data, file = 'gene_data.txt', row.names = FALSE,quote = FALSE,sep='\t')

## Expression table
# Identify columns to be extracted
sample_locations = which(samples %in% samp)
# extract gene expression from compressed data
expression = t(h5read(destination_file, "data/expression", index=list(sample_locations, 1:length(genes))))
H5close()
rownames(expression) = genes
colnames(expression) = samples[sample_locations]

# Print file
write.table(expression, file=extracted_expression_file, sep="\t", quote=FALSE, col.names=NA)
print(paste0("Expression file was created at ", getwd(), "/", extracted_expression_file))

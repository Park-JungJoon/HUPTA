library(data.table)
library(dplyr)
library(edgeR)

process_db_data <- function(genelen_filepath, rpk_output_filepath, getmm_output_filepath) {
  # reading file
  database <- fread(genelen_filepath, header = TRUE, sep = '\t')
  df_db <- as.data.frame(database)
  row.names(df_db) <- df_db$Gene
  df_db <- subset(df_db, select = -Gene)
  
  matrix_db <- as.matrix(df_db)
  
  # Calculate RPK
  rpk <- (matrix_tcga[, 2:ncol(matrix_db)] / matrix_db[, 1])
  matrix_db <- matrix_db[, -1]
  group <- c(rep("A", ncol(matrix_db)))
  
  # Save RPK output 
  write.table(rpk, file = rpk_output_filepath, quote = FALSE, sep = '\t')
  print('RPK calculation completed.')
  
  # GeTMM Normaliztion
  rpk_norm <- DGEList(counts = rpk, group = group)
  rpk_norm <- calcNormFactors(rpk_norm)
  norm_counts_rpk_edger <- cpm(rpk_norm)
  
  # Save GeTMM output
  write.table(norm_counts_rpk_edger, file = getmm_output_filepath, quote = FALSE, sep = '\t')
  print('GeTMM normalization completed.')
}

process_db_data("./Genlen_GEO.tsv","./RPK_GEO.tsv","GeTMM_GEO.tsv")
process_db_data("./Genlen_GTEx.tsv""./RPK_GTEx.tsv","GeTMM_GTEx.tsv")
process_db_data("./Genlen_TCGA.tsv","./RPK_TCGA.tsv","GeTMM_TCGA.tsv")

library(dplyr)
library(tidyr)
library(matrixStats)

geo_file <- "geo_expression.tsv"
gtex_file <- "gtex_expression.tsv"
tcga_file <- "tcga_expression.tsv"

geo <- read.table(geo_file, header = TRUE, sep = "\t", row.names = 1)
gtex <- read.table(gtex_file, header = TRUE, sep = "\t", row.names = 1)
tcga <- read.table(tcga_file, header = TRUE, sep = "\t", row.names = 1)

binarize_expression <- function(df) {
  df_bin <- df %>%
    mutate(across(everything(), ~ifelse(. >= quantile(., 0.75), 1, ifelse(. <= quantile(., 0.25), 0, NA))))
  df_bin[is.na(df_bin)] <- 0
  return(df_bin)
}

geo_bin <- binarize_expression(geo)
gtex_bin <- binarize_expression(gtex)
tcga_bin <- binarize_expression(tcga)

geo_sum <- rowSums(geo_bin)
gtex_sum <- rowSums(gtex_bin)
tcga_sum <- rowSums(tcga_bin)

z_score_normalize <- function(x) {
  return((x - mean(x)) / sd(x))
}

geo_z <- z_score_normalize(geo_sum)
gtex_z <- z_score_normalize(gtex_sum)
tcga_z <- z_score_normalize(tcga_sum)

cs_score <- rowMeans(cbind(geo_z, gtex_z, tcga_z))

cs_score_df <- data.frame(Gene = rownames(geo), CS_Score = cs_score)
write.table(cs_score_df, "cs_score.tsv", sep = "\t", row.names = FALSE, quote = FALSE)

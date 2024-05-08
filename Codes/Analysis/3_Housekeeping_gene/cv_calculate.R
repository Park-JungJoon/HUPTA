library('data.table')
cal_cv <- function(input,output,exp_output){
    # Load data; We used fread due to the large size of our data, but you can also use read.table.
    file = fread(input, sep = '\t', header = TRUE)
    # Gene should be located at column. If there are samples in columns, use t() function in R 
    gene = colnames(df.file)
    # Calculate coefficient of variants
    cv <- sapply(df.file,function(x) mean(x))
    cv_df <- merge(gene,cv)
    write.table(cv_df, file = output, quote = FALSE, sep = '\t')
}

geo_gct = "directory of geo gene count table"
geo_output = "directory of geo cv table"
gtex_gct = "directory of gtex gene count table"
gtex_output = "directory of gtex cv table"
tcga_gct = "directory of tcga gene count table"
tcga_output = "directory of tcga cv table"

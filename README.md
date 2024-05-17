# HUman Pan-Transcriptome Atlas (HUPTA)
Human transcriptome data have been accumulated in the public database such as [NCBI SRA](). Although attempts to compile/integrate all availabe public human transcriptome data have been reported [[refs]](), compiling all available human transcriptome data is not an easy task because of various factors - instrumental development, sequencing and analysis platform, and metadata inconsistency (e.g. gene names/categories). We collected publicly available human transcriptome data and developed a web application, designated as HUman Pan-Transcriptome Atlas (HUPTA) for gene-wise analysis of human transcriptome. Key features of gene expression were inspected in terms of tissue-specificity and expression regulation (constitutive - housekeeping - inducible...). [HUPTA]( https://ybq7u4-park-jungjoon.shinyapps.io/hupta/) is currently deployed on ```Shinyapp``` platform.

## Collected public transcriptome data
1. Gene Expression Omnibus - [GEO]()....
2. [GTEx]()....
3. [TCGA]()....
Each database...

+ The profile of a gene's tissue specificity, house keeping ability, and constitutive expression can be seen through a series of statistically calculated scores.
+ We collected 46,813 samples from three databases, GEO, GTEx, and TCGA, and obtained consensus on gene profiles.
+ Additionally, We provide promoter information from the [EPD]() database.

## Workflow


## Download HUPTA Dataset
Fully combined dataset is accessible in [here](). Also, you can analyze and access [HUPTA]() at the [```Shinyapp```]() application. 
+ By adjusting statistical parameters such as coefficient of variation, TAU, and fold change, users can download genes with the desired tissue specificity.

## Web Application requirments for local running.
See requirement.txt.

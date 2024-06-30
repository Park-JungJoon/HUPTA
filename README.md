# HUman Pan-Transcriptome Atlas (HUPTA)
Human transcriptome data have been accumulated in the public database such as [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra). Although attempts to compile/integrate all availabe public human transcriptome data have been reported [[refs]](https://maayanlab.cloud/archs4/), compiling all available human transcriptome data is not an easy task because of various factors - instrumental development, sequencing and analysis platform, and metadata inconsistency (e.g. gene names/categories). We collected publicly available human transcriptome data and developed a web application, designated as HUman Pan-Transcriptome Atlas (HUPTA) for gene-wise analysis of human transcriptome. Key features of gene expression were inspected in terms of tissue-specificity and expression regulation (constitutive - housekeeping). [HUPTA]( https://ybq7u4-park-jungjoon.shinyapps.io/hupta/) is currently deployed on ```Shinyapp``` platform.

## Collected public transcriptome data
1. Gene Expression Omnibus - [GEO](https://www.ncbi.nlm.nih.gov/geo/)
2. [GTEx](https://gtexportal.org/home/)
3. [TCGA](https://www.cancer.gov/ccg/research/genome-sequencing/tcga)

+ The profile of a gene's tissue specificity, house keeping ability, and constitutive expression can be seen through a series of statistically calculated scores.
+ We collected 46,813 samples from three databases, GEO, GTEx, and TCGA, and obtained consensus on gene profiles.
+ Additionally, We provide promoter information from the [EPD](https://epd.expasy.org/epd/) database.

## Workflow

![image](https://github.com/Park-JungJoon/HUPTA/assets/97942772/98093e7b-0b01-4d88-b599-36c2f0f6808b)

Four main steps to creating a HUPTA.

+ Download RNA-seq samples from publicly available RNA-seq databases
+ Processing RNA-seq data (normalization, filtering, manual scripting, calculating statistical values that can indicate tissue specificity and housekeeping expression ability)
+ The values obtained in the previous step are expressed as reliable scores such as TS score and CS score through consensus analysis.
+ The web application was published through Shiny for python.

## Download HUPTA Dataset
Fully combined dataset is accessible in [here](https://github.com/Park-JungJoon/HUPTA/blob/main/Codes/Analysis/6_Promoter_information/ESSENTIAL_17000_INFOS.tsv). Also, you can analyze and access [HUPTA](https://ybq7u4-park-jungjoon.shinyapps.io/hupta/) at the [```Shinyapp```](https://shiny.posit.co/py/) application. 
+ By adjusting statistical parameters such as coefficient of variation, TAU, and fold change, users can download genes with the desired tissue specificity.

## Web Application requirments for local running.
See requirement.txt.

# Workflow
Once all public data were downloaded, the raw count data first nomalized by sample and library sizes and integrated by gene name. Incosistency in human gene name among public data was resolved by unifying gene symbol with ENSG IDs.

## requirements
- R package
```
major          4                           
minor          4.0                         
year           2024                        
month          04                          
day            24                          
svn rev        86474                       
language       R                           
version.string R version 4.4.0 (2024-04-24)
nickname       Puppy Cup 
```
- RStudio
  
- Python 3.9.13

  
## Normalization
+  Gene length corrected trimmed mean of M-values [GeTMM](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2246-7) was used as the normalization method
+  GeTMM calculate RPK with edgeR with gene length normalization, scaling with library size.
+  To calculate GeTMM, we needed the gene length of each database, and we pre-calculated it by parsing the gtf for each database's gencode version.
+  Before using [GeTMM_calculate.R](HUPTA/Codes/Analysis/2_Intergrating_data_and_Normalization/GeTMM_calculate.R), Check requirements below.
  +  The column in gene count table should be configured as Gene/Gene length/Sample 1/Sample 2/... 
  +  Gene count table shold be a raw read count and shoud not be precdede by any processing such as gene filtering or tissue filtering.

---------
# Data intergrating

## Identify intersection gene 

+ The gencode annotation versions in the three databases are different (GTEx : 26, TCGA : 36, GEO : 41), We used 19,251 protein coding genes that matched based on ENSG number (excluding version).
+ Some of the ENSG numbers provided by ARCHS4 are missing, so we used [g:Profiler](https://biit.cs.ut.ee/gprofiler/gost) to replace gene symbols with ensg numbers.

## Meta data intergrating
+ The information provided by GTEX as meta data includes sample donor, tissue, specific tissue, submitted date, experiment method, sex, age, hardy scale, etc.
+ The information provided by TCGA as meta data includes age at tissue, diagnosis, race, sex, ethinicity, vital status, primary diagnosis, disease type.
+ The information provided by GEO as meta data includes tissue. For consensus analysis, we used only use tissue as metadata.
+ GTEx and TCGA have different terminology for tissues.
+ Manual matching was required and the tissues were categorized as described in [tissue_integrated.txt](HUPTA/Codes/Analysis/2_Intergrating_data_and_Normalization/tissue_integrated.txt).  
+ GEO categorizes tissues as described in the GEO description, we only used samples whose tissues in TCGA and GTEx matched the description exactly to get more accurate data.
+ Tissues with less than 100 samples for tissues present in the three databases were excluded from the analysis.
+ [Meta data file](HUPTA/Codes/Analysis/META_MAJOR_TISSUE.tsv)

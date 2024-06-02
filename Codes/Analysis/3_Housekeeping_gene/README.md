# House keeping gene analysis

## Workflow
1. Expression level pre-filtering (low expression level gene cause severe noise). Criteria : average expression was lower than 1 GeTMM in the higest tissue. 
2. Calculate coefficient of variation (CV), Fold Change(FC) in each data base per gene. (cv_calculate.R)
3. Make house keeping gene candidate in each database (CV bottom 1st quartile, FC pre-filtering 4).

## Requirements


#### Expression level pre-filtering
+ we excluded from the analysis those genes whose average expression was lower than 1 GeTMM in the highest tissue, even in one database, to avoid severe noise.

#### Calculate CV, FC
+ Coefficient of variation. The coefficient of Variation (CV) is defined as the ratio of the standard deviation. We adopted CV instead of standard deviation, because the library sizes of each sample are not equal. CV values range from 0 to 1. A value closer to 0 indicates a more housekeeping pattern. [code](https://github.com/Park-JungJoon/HUPTA/blob/main/Codes/Analysis/3_Housekeeping_gene/cv_calculate.R)
+ Fold change. For a house keeping gene, this is the ratio of the average expression level in the tissue with the highest expression to the average expression level in the tissue with the lowest expression. We use fold change as a pre-filtering criterion.We pre-filtered genes with an average fold change (FC) of 4 or higher and defined genes with an average coefficient of variation (CV) in the lower 25% across the three databases as housekeeping Genes (HKG). You can adjust the criteria on the download page to customize your downloads.
   

#### House keeping gene candidate in each database

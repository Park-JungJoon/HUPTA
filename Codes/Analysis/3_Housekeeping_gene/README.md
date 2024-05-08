# House keeping gene analysis
##### HUPTA used two paramteres to define the house keeping gene. 
  + Coefficient of variation. The coefficient of Variation (CV) is defined as the ratio of the standard deviation. We adopted CV instead of standard deviation, because the library sizes of each sample are not equal. CV values range from 0 to 1. A value closer to 0 indicates a more housekeeping pattern.
  + Fold change. For a house keeping gene, this is the ratio of the average expression level in the tissue with the highest expression to the average expression level in the tissue with the lowest expression. We use fold change as a pre-filtering criterion.We pre-filtered genes with an average fold change (FC) of 4 or higher and defined genes with an average coefficient of variation (CV) in the lower 25% across the three databases as housekeeping Genes (HKG). You can adjust the criteria on the download page to customize your downloads.
  + Additionally,  we excluded from the analysis those genes whose average expression was lower than 1 GeTMM in the highest tissue, even in one database, to avoid severe noise.

## Method
##### Following the attached code, we calculated CV and FC for each database. After expression level pre-filtered, we defined housekeeping genes as those with CV in the bottom 25% and FC not exceeding 4 among 17,151 protein coding genes. 

# Data intergrating

## Gene intergrating

+ The gencode annotation versions in the three databases are different (GTEx : 26, TCGA : 36, GEO : 41), We used 19,251 protein coding genes that matched based on ENSG number (excluding version).
+ Some of the ENSG numbers provided by ARCHS4 are missing, so we used [g:Profiler](https://biit.cs.ut.ee/gprofiler/gost) to replace gene symbols with ensg numbers.

## Meta data intergrating
+ 

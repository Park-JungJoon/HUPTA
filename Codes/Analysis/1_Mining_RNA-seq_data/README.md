# 친절한 절차 설명과 함께 다운로드받은 데이터의 기초통계와 함께 링크를 넣고 업데이트하세요

## This directory contains HOWTOs for collecting RNA-seq data (raw read counts) and metadata.
We focused on three databases for collecting transcriptome data using on RNA-seq.
1. GTEx
2. ..
3. ..
   
## GTEx database (as of Apr 2024) ver. 7??
There are several raw data provided by the [GTEx database]() that is freely accessible. We downloaded the data directly from the database using ```wget``` command in the Linux environment.

### GTEx gene count table mining

~~~
wget https://storage.googleapis.com/adult-gtex/bulk-gex/v8/rna-seq/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.gct.gz
~~~

### GTEx meta data mining

~~~
wget https://storage.googleapis.com/adult-gtex/annotations/v7/metadata-files/GTEx_Analysis_v7_Annotations_SampleAttributesDD.xlsx
wget https://storage.googleapis.com/adult-gtex/annotations/v7/metadata-files/GTEx_Analysis_v7_Annotations_SubjectPhenotypesDD.xlsx
wget https://storage.googleapis.com/adult-gtex/annotations/v7/metadata-files/GTEx_v7_Annotations_SampleAttributesDS.txt
wget https://storage.googleapis.com/adult-gtex/annotations/v7/metadata-files/GTEx_v7_Annotations_SubjectPhenotypesDS.txt
~~~


<br/>

## TCGA data collecting
### TCGA gene count table mining
+ Download all available files in TCGA, with json format.
+ Extract case id from json file using gdc-client to collect gene count table.

~~~
gdc_client_tcga_download.py
~~~


### TCGA meta data mining
+ Download all available files's metadata in TCGA, with json format.

<br/>

## GEO (ARCHS4) data collecting
+ Both meta data and gene count table were obtained by parsing the h5 format file through the code below. 
~~~
handling_archs4.R
~~~

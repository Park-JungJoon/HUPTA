# Workflow

1. Raw read count table download
2. Meta data download


Database	|Samples	|Gene Annotation Version	|Protein Coding Gene|	Non-Protein Coding Gene|	Total Gene|	Expression filtered gene	|Metadata	|Annotation program
-|-|-|-|-|-|-|-|-
GTEx|	17,382	|26|	19,291|	35,910|	56,201|	18,217	|Tissue, Sex, Age	|STAR
TCGA|	22,018	|36|	19,962|	40,699|	60,661|	18,189	|Tissue, Sex, Age|	STAR
GEO	|12,393|	41	|19,598|	42,951	|62,540|	17,564	|Tissue|	Kallisto



## This directory contains HOWTOs for collecting RNA-seq data (raw read counts) and metadata.
We focused on three databases for collecting transcriptome data using on RNA-seq.
1. GTEx
2. TCGA
3. GEO (ARCHS4)
   
## GTEx database (V8 2017.06)
There are several raw data provided by the [GTEx database](https://gtexportal.org/home/) that is freely accessible. We downloaded the data directly from the database using ```wget``` command in the Linux environment.

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

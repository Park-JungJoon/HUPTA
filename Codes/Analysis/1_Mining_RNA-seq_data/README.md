# Download RNAseq data
This directory contains scripts for collecting RNA-seq data (raw read counts) and metadata.
<br/>
## GTEx data collecting
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

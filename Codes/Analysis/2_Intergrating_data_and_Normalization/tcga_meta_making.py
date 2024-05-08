import math
import json
from collections import defaultdict
infofile = defaultdict(list)
infocase = defaultdict(list)
# raw data : json files from TCGA
# parsing object : meta data for each gene count table file names
with open ('./files20221221.json') as f:
    file = json.load(f)

with open ('./cases.2022-12-22.json') as g:
    case = json.load(g)

for i in file:
    fileid = i['file_id']
    filename = i['file_name']
    caseid = i['cases'][0]["case_id"]
    infofile[filename] = caseid

for i in case:
    caseid = i["case_id"]

    if "primary_site" not in i.keys() or i["primary_site"] == None:
        tissue = "NA"
    else:
        tissue = i["primary_site"] #i is one case   

    if "disease_type" not in i.keys() or i["disease_type"] == None:
        disease = "NA"
    else:
        disease = i["disease_type"]

    if "diagnoses" not in i.keys():
        ageatdig = 'NA'
        description = 'NA'
    else:
      if "age_at_diagnosis" not in i["diagnoses"][0].keys() or i["diagnoses"][0]["age_at_diagnosis"] == None:
        ageatdig = 'NA'
      else:
        ageatdig = i["diagnoses"][0]["age_at_diagnosis"]

      if "primary_diagnosis" not in i["diagnoses"][0].keys():
        description = 'NA'
      else: 
        description = i["diagnoses"][0]["primary_diagnosis"]

    if "demographic" not in i.keys():
        sex = 'NA'
    else:
      if "gender" not in i['demographic'].keys():
        sex = 'NA'
      else:
        sex = i["demographic"]["gender"]


    if tissue == 'NA':
        continue
        print(caseid)
    
    if ageatdig == 'NA':
        pass
    else:
        ageatdig = int(ageatdig)/365
        ageatdig = str(ageatdig) 
        ageatdig = str(ageatdig[0])+'0-'+str(ageatdig[0])+'9'
    infocase[caseid].append(tissue)
    infocase[caseid].append(tissue)
    infocase[caseid].append(sex)
    infocase[caseid].append(ageatdig)
    infocase[caseid].append(disease+';'+description)
with open ('./meta_tcga.tsv','w') as h:
    for k,v in infofile.items():
        k = k.replace('.rna_seq.augmented_star_gene_counts.tsv','')
        stri = 'TCGA'+'\t'+k + '\t' + '\t'.join(infocase[v])
        h.write(stri + '\n')

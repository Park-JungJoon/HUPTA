import os
import pandas as pd
from collections import defaultdict
from parser import gene_setting
from parser import hkg_return
from parser import ts_return
media = os.getcwd()
genes = ["Example"]
genes = genes + list(gene_setting()[0])
essential_genes = gene_setting()[1]
nonessential_genes = list(set(genes) - set(essential_genes))
hkgdic = hkg_return()
ts_dic = ts_return()[0]
promoter_dic = ts_return()[1]    
nonepd_genes = list(set(genes) - set(list(promoter_dic.keys())))


def hkg_table_showing(gene):
    if gene == 'Example':
        hkg_table = pd.DataFrame({'Database': ['Mean', 'GEO', 'GTEx', 'TCGA'],
                                  'CV': ['NA', 'NA', 'NA', 'NA'],
                                  'FoldChange': ['NA', 'NA', 'NA', 'NA']})
    elif gene in nonessential_genes:
        hkg_table = pd.DataFrame({'Database': ['Mean', 'GEO', 'GTEx', 'TCGA'],
                                  'CV': ['NA', 'NA', 'NA', 'NA'],
                                  'FoldChange': ['NA', 'NA', 'NA', 'NA']})
    else:
        hkg_table = pd.DataFrame({'Database': ['Mean', 'GEO', 'GTEx', 'TCGA'],
                                  'CV': [str(round(float(hkgdic[gene]["Mean CV"]),6)),
                                         str(round(float(hkgdic[gene]["GEO CV"]),6)),
                                         str(round(float(hkgdic[gene]["GTEx CV"]),6)),
                                         str(round(float(hkgdic[gene]["TCGA CV"]),6))],
                                  'FoldChange': [str(round(float(hkgdic[gene]["Mean FC"]),6)),
                                                 str(round(float(hkgdic[gene]["GEO FC"]),6)),
                                                 str(round(float(hkgdic[gene]["GTEx FC"]),6)),
                                                 str(round(float(hkgdic[gene]["TCGA FC"]),6))]})

    return hkg_table

def ts_table_showing(gene):
    if gene == 'Example':
        ts_table = pd.DataFrame({'Database': ['Mean', 'GEO', 'GTEx', 'TCGA'],
                                 'NTau': ['NA', 'NA', 'NA', 'NA'],
                                 'NFC': ['NA', 'NA', 'NA', 'NA']})
    elif gene in nonessential_genes:
        ts_table = pd.DataFrame({'Database': ['Mean', 'GEO', 'GTEx', 'TCGA'],
                                  'NTau': ['NA', 'NA', 'NA', 'NA'],
                                  'NFC': ['NA', 'NA', 'NA', 'NA']})
 
    else:
        ts_table = pd.DataFrame({'Database': ['Mean', 'GEO', 'GTEx', 'TCGA'],
                                 'NTau': [str(round(float(ts_dic[gene]["Mean Z-Tau"]),6)),
                                         str(round(float(ts_dic[gene]["GEO Z-Tau"]),6)),
                                         str(round(float(ts_dic[gene]["GTEx Z-Tau"]),6)),
                                         str(round(float(ts_dic[gene]["TCGA Z-Tau"]),6))],
                                 'NFC': [str(round(float(ts_dic[gene]["Mean Z-LogFC"]),6)),
                                                str(round(float(ts_dic[gene]["GEO Z-LogFC"]),6)),
                                                str(round(float(ts_dic[gene]["GTEx Z-LogFC"]),6)),
                                                str(round(float(ts_dic[gene]["TCGA Z-LogFC"]),6))]})
    return ts_table

def promoter_table(gene):
    tmpdic = {}
    if gene in nonepd_genes:
        answer = pd.DataFrame({"Promoter" : "Not in EPD DB",
              "Promoter Type" : "NA",
              "Promoter Motifs" : "NA",
              "Promoter Sequence": "NA"}, index = [0])
        return (answer)
    elif gene == 'Example':
        promoters = ['example_promoter']
        promoter_type = ['Type of promoter']
        promoter_motifs = ['Motifs in promoter']
        promoter_sequences = ['-50 ~ 10 bp from initiation site']
        tmpdic = {}
        tmpdic['Promoter'] = promoters
        tmpdic['Promoter Type'] = promoter_type
        tmpdic['Promoter Motifs'] = promoter_motifs
        tmpdic['Promoter Sequences'] = promoter_sequences
        answer = pd.DataFrame.from_dict(tmpdic)
        return(answer)  
    else:
        promoters_list = promoter_dic[gene] # DICTIONARY
        promoter_name = []
        promoter_type = [] 
        promoter_motifs = []
        promoter_sequences = []
        for promoter_small_dic in promoters_list:
            promoter_name.append(promoter_small_dic["Promoter"])
            promoter_type.append(promoter_small_dic["Promoter Type"])
            promoter_motifs.append(promoter_small_dic["Promoter Motifs"])
            promoter_sequences.append(promoter_small_dic["Promoter Sequence"])
        tmpdic['Promoter']  = promoter_name
        tmpdic['Promoter Type'] = promoter_type
        tmpdic['Motifs in Promoter'] = promoter_motifs
        tmpdic['Promoter Sequence'] = promoter_sequences
        answer = pd.DataFrame.from_dict(tmpdic)
        return(answer)

def tissue_table(gene):
    if gene == "Example":
        tissue = pd.DataFrame({'Database' : ['GEO','GTEx','TCGA'],
                          'Tissue' : ["Most Expressed Tissue in GEO","Most Expressed Tissue in GTEx","Most Expressed Tissue in TCGA"]})
        return(tissue)
    
    elif gene in nonessential_genes:
        tissue = pd.DataFrame({'Database' : ['GEO','GTEx','TCGA'],'Tissue' : ["Not Detected","Not Detected","Not Detected"]})
        return(tissue)
    
    else:
        tissue = pd.DataFrame({'Database' : ['GEO','GTEx','TCGA'],
                          'Tissue' : [ts_dic[gene]["GEO Tissue"],ts_dic[gene]["GTEX Tissue"],ts_dic[gene]["TCGA Tissue"]]})
        return(tissue)

for gene in genes:
    hkg_table = hkg_table_showing(gene)
    ts_table = ts_table_showing(gene)
    promoter_tab = promoter_table(gene)
    promoter_tab = promoter_tab.drop_duplicates()
    promoter_tab = promoter_tab.sort_values(by='Promoter')
    t_table = tissue_table(gene)
    mediadir = media + '/dataframes/'
    hkg_table.to_csv(mediadir+ 'hkg/'+ gene+'.tsv', sep = '\t',index = False)
    ts_table.to_csv(mediadir+ 'ts/'+ gene+'.tsv',sep = '\t', index = False)
    promoter_tab.to_csv(mediadir+ 'promoter/'+ gene+'.tsv',sep = '\t', index = False)
    t_table.to_csv(mediadir + 'tissue/'+gene+'.tsv',sep = '\t', index = False)

import random
from datetime import datetime
import os
from collections import defaultdict
import json
media = os.getcwd() + '/media'
with open(media + '/input/main_gene_info.json', "r") as file:
    main_dict = json.load(file)

def ts_download_parser(tissue, ts_score, consititive_score, consensus_percentile):  #return tab separated list
    answer = []
    for k,v in main_dict.items():
        if v["TS score"] == 'Not Detected':
            continue
        if float(v["TS score"]) < float(ts_score):
            continue
        if v["Tissue"] not in tissue:
            continue
        if float(v["Constitive"]) < float(consititive_score):
            continue
        if float(v["Consensus"]) < float(consensus_percentile):
            continue
        tmpanswer = k + '\t' + v["Tissue"]
        answer.append(tmpanswer)
    return(answer) #Gene\tTissue

def up_down_parser (tissue, ud): #return tab separated list
    answer = []
    for k,v in main_dict.items():
        if ud == 'up':
            correct = list(set(tissue) & set(v["Regulate"]["Up"]))
            if len(correct) != 0:
                answer.append(k + '\t' + '\t'.join(correct) + '\t' + 'Up')
        if ud == 'down':
            correct = list(set(tissue) & set(v["Regulate"]["Down"]))
            if len(correct) != 0:
                answer.append(k + '\t' + '\t'.join(correct)+ '\t' + 'Down')
    return(answer) #Gene\tTissue


def gene_hkg_infos(): 
    dic = defaultdict(list)
    with open (media + '/input/hkg_merged_all.tsv') as f:
        lines = f.readlines()
        for line in lines[1:]:
            gene = line.split('\t')[0]
            geo_cv = line.split('\t')[1]
            gtex_cv = line.split('\t')[3]
            tcga_cv = line.split('\t')[5]
            mean_fc = (float(line.split('\t')[2]) + float(line.split('\t')[4]) +float(line.split('\t')[6]))/3
            tmplist = [geo_cv, gtex_cv, tcga_cv, mean_fc]
            dic[gene] = tmplist
        return(dic)

def  hkg_download_parser(cv, fc, constitive, union): #return list
    cv_dic = {}
    with open (media + "/input/cv_percentile.tsv") as f:
        lines = f.readlines()
        for line in lines[1:]:
            percentile = float(line.split('\t')[0])
            geo_cv = float(line.split('\t')[1])
            gtex_cv = float(line.split('\t')[2])
            tcga_cv = float(line.split('\t')[3])
            cvlist = [geo_cv,gtex_cv,tcga_cv]
            cv_dic[percentile] = cvlist
    hkg_infos_dic = gene_hkg_infos()
    geo_pass = []
    gtex_pass = []
    tcga_pass = []
    for gene,cvlist in hkg_infos_dic.items():
        geo = float(cvlist[0])
        gtex = float(cvlist[1])
        tcga = float(cvlist[2])
        foldchange = float(cvlist[3])
        if geo < cv:
            if foldchange < fc: 
                geo_pass.append(gene)
        if gtex < cv:
            if foldchange < fc: 
                gtex_pass.append(gene)
        if tcga < cv:
            if foldchange < fc: 
                tcga_pass.append(gene)
    constitive_pass = []
    for k in main_dict.keys():
        if constitive < float(main_dict[k]['Constitive']):
            constitive_pass.append(k)
    if union == 'intersect':
        answer = list(set(geo_pass) & set(gtex_pass) & set(tcga_pass) & set(constitive_pass))
    if union == 'union':
        answer = list((set(geo_pass) | set(gtex_pass) | set(tcga_pass))  & set(constitive_pass))
    return(answer)

allgenes = []
essentialgenes = []
def gene_setting():
    with open (media + '/input/allgenes.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            allgenes.append(line)
    with open (media+ '/input/overexpgenes.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            essentialgenes.append(line)
    return [allgenes,essentialgenes]

def file_write(my_list,string_input):
    random_number = random.randint(100, 999)
    current_date = datetime.now().strftime('%Y_%m_%d')
    filename = f"{string_input}_{current_date}_{random_number}.txt"
    root = media + '/tmp/'
    with open(root + filename, 'w') as file:
        for item in my_list:
            file.write(str(item) + '\n')
    return(root+filename)

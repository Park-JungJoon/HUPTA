import math
from collections import defaultdict
# Input file should be a tissue mean expression table in TSV format
# Tissue located in column, Gene located in row name
geo_file_dir = "/eevee/val/jjpark/PAPER_RNA_SEQ_ATLAS/ts_scoring_new/raw_input/r_T_MEAN_GEO_TISSUE_GCT.tsv"
gtex_file_dir = "/eevee/val/jjpark/PAPER_RNA_SEQ_ATLAS/ts_scoring_new/raw_input/r_T_MEAN_GTEX_TISSUE_GCT.tsv"
tcga_file_dir = "/eevee/val/jjpark/PAPER_RNA_SEQ_ATLAS/ts_scoring_new/raw_input/r_T_MEAN_TCGA_TISSUE_GCT.tsv"

geo = defaultdict(list)
gtex = defaultdict(list)
tcga = defaultdict(list)

# Tau calculate in each gene per database
def calculate_tau(line):
    line = line.rstrip()
    exps = line.split('\t')[1:]
    exps = [float(i) for i in exps]
    gene = line.split('\t')[0]
    max_exp = max(exps)
    if max_exp == 0:
        tau = 0
        return [gene,tau]
    xi = []
    for exp in exps:
        xi_tmp = exp / max_exp
        xi.append(xi_tmp)
    tau = 0
    for x in xi:
        tau += 1-x
    return [gene,tau]

# Fold change calculate in each gene per database
def calculate_fc(line):
    line = line.rstrip()
    exps = line.split('\t')[1:]
    exps = [float(i) for i in exps]
    gene = line.split('\t')[0]
    max_exp = max(exps)
    sec_exps = sorted(exps,reverse=True)[1]
    fc = math.log2(max_exp + 1.001) / math.log2(sec_exps + 1.001)
    return [gene,fc]

# Read file and save in dictionary
with open (geo_file_dir) as f:
    lines = f.readlines()
    for line in lines[1:]:
        c1 = calculate_tau(line)
        c2 = calculate_fc(line)
        gene = c1[0]
        tau = c1[1]
        fc = c2[1]
        geo[gene] = [str(tau),str(fc)]

with open (gtex_file_dir) as f:
    lines = f.readlines()
    for line in lines[1:]:
        c1 = calculate_tau(line)
        c2 = calculate_fc(line)
        gene = c1[0]
        tau = c1[1]
        fc = c2[1]
        gtex[gene] = [str(tau),str(fc)]


with open (tcga_file_dir) as f:
    lines = f.readlines()
    for line in lines[1:]:
        c1 = calculate_tau(line)
        c2 = calculate_fc(line)
        gene = c1[0]
        tau = c1[1]
        fc = c2[1]
        tcga[gene] = [str(tau),str(fc)]

with open ("ts_score_tau_fc.tsv", "w") as f:
  f.write("Gene\tGEO_Tau\tGEO_FC\tGTEx_Tau\tGTEx_FC\tTCGA_Tau\tTCGA_FC\n")
  for k,v in geo.items():
    f.write(k + '\t' + v[0] +'\t'+v[1]+ '\t' + gtex[k][0] +'\t'+ gtex[k][1] +'\t'+ tcga[k][0]+'\t'+tcga[k][1]+'\n')

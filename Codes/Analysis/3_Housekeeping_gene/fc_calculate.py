import numpy as np
from collections import defaultdict
# Input file is a table with the calculated average expression per tissue in the database.
# Input file's column is gene.
# Fold change in HKG analysis is  is the average expression of the most highly expressed tissue / average expression of all tissues.
def hkg_fc_cal (file_path):
    dict = defaultdict(int)
    with open (file_path) as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.rstrip()
                gene = line.split('\t')[0]
                exp = line.split('\t')[1:]
                exp = [float(i) for i in exp]
                maxexp = max(exp)
                meanexp = np.mean(exp)
                fc = maxexp/meanexp
                dict[gene] = str(fc)
            return(dict)

geo = "./r_T_MEAN_GEO_TISSUE_GCT.tsv"
gtex = "./r_T_MEAN_GTEX_TISSUE_GCT.tsv"
tcga = "./r_T_MEAN_TCGA_TISSUE_GCT.tsv"

geo_dict = hkg_fc_cal(geo)
gtex_dict = hkg_fc_cal(gtex)
tcga_dict = hkg_fc_cal(tcga)

with open ("./allgenes_fc_forhkg_geo.tsv","w") as g:
    g.write('Gene\tFC\n')
    for k,v in geo_dict.items():
        g.write(k+'\t'+v+'\n')

with open ("./allgenes_fc_forhkg_gtex.tsv","w") as g:
    g.write('Gene\tFC\n')
    for k,v in gtex_dict.items():
        g.write(k+'\t'+v+'\n')

with open ("./allgenes_fc_forhkg_tcga.tsv","w") as g:
    g.write('Gene\tFC\n')
    for k,v in tcga_dict.items():
        g.write(k+'\t'+v+'\n')

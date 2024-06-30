from collections import defaultdict
import os 
media = os.getcwd() # parser.py should be located in media dir
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

lowexp_genes = list(set(allgenes)-set(essentialgenes))

hkgs = []
hkgdic = defaultdict(dict)
def hkg_return():
    with open (media + "/input/HKGs_25percentile.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            hkgs.append(line)
    with open (media + "/input/hkg_merged_all.tsv") as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.rstrip()
            gene = line.split('\t')[0]
            if gene in lowexp_genes:
                hkgdic[gene]["Consensus"] = "Low"
            else:
                hkgdic[gene]["Consensus"] = "High"
            cv_geo = line.split('\t')[1]
            fc_geo = line.split('\t')[2]
            cv_gtex = line.split('\t')[3]
            fc_gtex = line.split('\t')[4]
            cv_tcga = line.split('\t')[5]
            fc_tcga = line.split('\t')[6]
            mean_cv = str((float(cv_geo) + float(cv_tcga) + float(cv_gtex))/3)
            mean_fc = str((float(fc_geo) + float(fc_tcga) + float(fc_gtex))/3)
            if gene in hkgs:
                define_hkg = "HKG"
            else:
                define_hkg = "No HKG"
            hkgdic[gene]["HKG"] = define_hkg
            hkgdic[gene]["Mean CV"] = mean_cv
            hkgdic[gene]["Mean FC"] = mean_fc
            hkgdic[gene]["GEO CV"] = cv_geo
            hkgdic[gene]["GTEx CV"] = cv_gtex
            hkgdic[gene]["TCGA CV"] = cv_tcga
            hkgdic[gene]["GEO FC"] = fc_geo
            hkgdic[gene]["GTEx FC"] = fc_gtex
            hkgdic[gene]["TCGA FC"] = fc_tcga
    return hkgdic

tsdic = defaultdict(dict)
promoterdic = defaultdict(list)
notinepddb = {"Promoter" : "Not in EPD DB",
              "Promoter Type" : "NA",
              "Promoter Motifs" : "NA",
              "Promoter Sequence": "NA"}
def ts_return():
    with open (media + "/input/ESSENTIAL_17000_INFOS.tsv") as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.rstrip()
            gene = line.split('\t')[0]
            ts_geo = line.split('\t')[1]
            ts_gtex = line.split('\t')[2]
            ts_tcga = line.split('\t')[3]
            predicted_tissue = line.split('\t')[4]
            geo_tissue = line.split('\t')[5]
            gtex_tissue = line.split('\t')[6]
            tcga_tissue = line.split('\t')[7]
            ts_score = line.split('\t')[8]
            zlogfc_geo = line.split('\t')[9]
            zlogfc_gtex = line.split('\t')[10]
            zlogfc_tcga = line.split('\t')[11]
            zlogfc_mean = str((float(zlogfc_geo) + float(zlogfc_gtex) + float(zlogfc_tcga))/3)
            ztau_geo = line.split('\t')[12]
            ztau_gtex = line.split('\t')[13]
            ztau_tcga = line.split('\t')[14]
            ztau_mean = str((float(ztau_geo) + float(ztau_gtex) + float(ztau_tcga))/3)
            promoter_all_infos = line.split('\t')[-1]
            if promoter_all_infos == "Not in EPD DB":
                promoterdic[gene].append(notinepddb)
            else:
                promoters_infos = promoter_all_infos.split('/')
                for promoter_info in promoters_infos:
                    tmpdic = defaultdict(str)
                    promoter = promoter_info.split(';')[0]
                    promoter_type = promoter_info.split(';')[1]
                    promoter_sequence = promoter_info.split(';')[-1]
                    expdic = [promoter, promoter_type, promoter_sequence]
                    promoter_motifs_tmp = promoter_info.split(';')
                    promoter_motifs = []
                    for pmotif in promoter_motifs_tmp:
                        if pmotif not in expdic:
                            promoter_motifs.append(pmotif)
                    promoter_motifs = sorted(promoter_motifs)
                    tmpdic["Promoter"] = promoter
                    tmpdic["Promoter Type"] = promoter_type
                    tmpdic["Promoter Sequence"] = promoter_sequence
                    tmpdic["Promoter Motifs"] = ','.join(promoter_motifs)
                    promoterdic[gene].append(tmpdic) 
            tsdic[gene]["TS score"] = ts_score
            tsdic[gene]["GEO TS"] = ts_geo
            tsdic[gene]["GTEX TS"] = ts_gtex
            tsdic[gene]["TCGA TS"] = ts_tcga
            tsdic[gene]["Mean Z-LogFC"] = zlogfc_mean
            tsdic[gene]["GEO Z-LogFC"] = zlogfc_geo
            tsdic[gene]["GTEx Z-LogFC"] = zlogfc_gtex
            tsdic[gene]["TCGA Z-LogFC"] = zlogfc_tcga
            tsdic[gene]["Mean Z-Tau"] = ztau_mean
            tsdic[gene]["GEO Z-Tau"] = ztau_geo
            tsdic[gene]["GTEx Z-Tau"] = ztau_gtex
            tsdic[gene]["TCGA Z-Tau"] = ztau_tcga
            tsdic[gene]["GEO Tissue"] = geo_tissue
            tsdic[gene]["GTEX Tissue"] = gtex_tissue
            tsdic[gene]["TCGA Tissue"]  = tcga_tissue
            tsdic[gene]["Predicted Tissue"] = predicted_tissue
        for gene in lowexp_genes:
            tsdic[gene]["TS score"] = "Not Detected"
            tsdic[gene]["GEO TS"] = "Not Detected"
            tsdic[gene]["GTEX TS"] = "Not Detected"
            tsdic[gene]["TCGA TS"] = "Not Detected"
            tsdic[gene]["Mean Z-LogFC"] = "Not Detected"
            tsdic[gene]["GEO Z-LogFC"] = "Not Detected"
            tsdic[gene]["GTEx Z-LogFC"] = "Not Detected"
            tsdic[gene]["TCGA Z-LogFC"] = "Not Detected"
            tsdic[gene]["Mean Z-Tau"] = "Not Detected"
            tsdic[gene]["GEO Z-Tau"] = "Not Detected"
            tsdic[gene]["GTEx Z-Tau"] = "Not Detected"
            tsdic[gene]["TCGA Z-Tau"] = "Not Detected"
            tsdic[gene]["GEO Tissue"] = "Not Detected"
            tsdic[gene]["GTEX Tissue"] = "Not Detected"
            tsdic[gene]["TCGA Tissue"]  = "Not Detected"
            tsdic[gene]["Predicted Tissue"] = "Not Detected"
        return([tsdic,promoterdic])


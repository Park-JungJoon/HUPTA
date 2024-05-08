import pandas as pd
using = ['Bladder','Brain','Kidney','Spleen','Liver','Blood','Uterus',
        'Lung','Breast','Small Intestine','Thyroid','Stomach','Testis','Skin','Prostate','Pituitary','Adipose Tissue',
        'Vagina','Blood Vessel','Adrenal Gland','Pancreas','Heart','Esophagus','Large intestine',
        'Ovary','Thymus','Muscle']

with open ('./raw_archs4_meta.txt') as f:
    lines =f.readlines()
    for line in lines:
        line = line.rstrip()
        smp = line.split('\t')[1]
        tis = line.split('\t')[2]
        if tis not in using:
            continue
        print(line)

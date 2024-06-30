from collections import defaultdict
ensdic = {}
with open ('matching_3cushion.tsv') as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        sym = line.split('\t')[1]
        ensg = line.split('\t')[0]
        ensdic[sym] = ensg
with open ('promoter_ensembl.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        pmt = line.split('\t')[0].split('_')[0]
        ensg = line.split('\t')[1]
        ensdic[pmt] = ensg

with open ('promoter_sequence.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        pmt = line.split('\t')[0]
        seq = line.split('\t')[1]
        #seq = seq.replace('a','')
        #seq = seq.replace('t','')
        #seq = seq.replace('c','')
        #seq = seq.replace('g','')
        if pmt.split('_')[0] not in ensdic:
            continue
        print(pmt + '\t' + ensdic[pmt.split('_')[0]] + '\t'+ seq)

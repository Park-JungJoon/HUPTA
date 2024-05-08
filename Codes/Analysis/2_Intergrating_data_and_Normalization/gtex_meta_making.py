from collections import defaultdict
dic = defaultdict(list)
with open ('./GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt') as f:
    lines = f.readlines()
    for line in lines[1:]:
        line = line.rstrip()
        gtexid = line.split('\t')[0]
        description = line.split('\t')[3]
        age = line.split('\t')[2]
        sex = sex.replace('1','male')
        sex = sex.replace('2','female')
        dic2[humanid].append(sex)
        dic2[humanid].append(age)


for k in dic.keys():
    humid = '-'.join(k.split('-')[0:2])
    for i in dic2[humid]:
        dic[k].append(i)

for k, v in dic.items():
    print(k+'\t'+'-'.join(k.split('-')[0:2])+'\t'+'\t'.join(v))

import os
import json
with open ('./files20221221.json') as f:
    file = json.load(f)
for i in range(len(file)):
    os.system("./gdc-client download %s" %file[i]['file_id'])

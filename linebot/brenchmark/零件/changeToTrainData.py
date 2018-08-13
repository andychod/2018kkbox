import json

'''def change(lys):
    lys = lys.split('\n')
    newlys = []
    for data in lys:
        if(data != ""):
            newlys.append(data)
    return newlys'''

with open('clusterData.json', 'r',encoding="'utf-8-sig'") as f:
    file = json.load(f)

output = []
for i in range(len(file)):
    tail = ""
    for data in file[i]['lys']:
        output.append(data)
        tail = data
    output.append(tail)


with open('trainData.json', 'w',encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False,indent=4)
    f.close()

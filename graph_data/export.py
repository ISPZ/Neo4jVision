import json
import codecs



dicts = []
with open('military_sys.json','r') as f:
    militarysys_dict = {}
    cont = 0
    jsons = json.load(f)
    # militarysys_dict['cate']=jsons
    print(jsons)
    cont = 16
    for jsstr in jsons:       
        militarysys_dict['name']=jsstr
        militarysys_dict['category']=cont
        # militarysys_dict['source'] = jsstr[0]
        # militarysys_dict['target']= jsstr[1]
        # militarysys_dict['value']= '属于'
        cont += 1
        dicts.append(militarysys_dict.copy()) #注意.copy()
        # print(militarysys_dict)
        print(dicts)
        print(jsstr)
    
       

        

with codecs.open('txt1.json', 'w+', encoding='utf-8') as f:
    json.dump(dicts, f, indent=4, ensure_ascii=False)

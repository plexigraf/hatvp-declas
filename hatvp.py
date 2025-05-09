import xml,json,xmltodict
from datetime import date
#from modif_nested_diff import diff, patch #modified official nested_diff package
import sys
import collections
import os
import shutil




sample=False #20 premieres entrees uniquement (pour dev)
sampleStr="-sample-" if sample else ""
compute_diffs=False
output_by_job=False


xmlfilename=sys.argv[1] if len(sys.argv)>1 else 'declarations.xml'


verbosis=False

today = str(date.today())
print( xmlfilename,today)

#save=False


def verbose(*args,**kwargs):
    if verbosis:
        print(*args,**kwargs)

def printjs(s):
    verbose(json.dumps(s, indent=4, sort_keys=True, ensure_ascii=False))




with open(xmlfilename, "r+") as xmlFile:
   obj = xmltodict.parse(xmlFile.read(), encoding='utf-8')['declarations']['declaration']


if sample:
	obj=obj[0:20]

def compare(d1,d2):
    #compare dates
	d1=d1.split('/')
	d2=d2.split('/')
	return True if d1[2]>d2[2] else (True if d1[1]>d2[1] else True if d1[0]>d2[0] else False)

result={}#>declas.json
last_result={}#>derniers_declas.json

mandats=['tout']


for i in obj:
    nom=i['general']['declarant']['nom']+', '+i['general']['declarant']['prenom']
    date_elts=i['dateDepot'].split(' ')[0].split('/')+[i['dateDepot'].split(' ')[1]]
    key=nom+' - '+date_elts[2]+'-'+date_elts[1]+'-'+date_elts[0]+'-'+date_elts[3]
    print(key)
    mandat=i['general']['qualiteMandat']['typeMandat']
    print(mandat)
    mandats+=[mandat]#semble equiv a 'codTypeMandatFichier' et mieux que 'qualiteDeclarantForPDF'  'labelTypeMandat'
    clean_entry={'mandat':mandat}
    for k in i:
    	if 'neant' in i[k]:
    		if i[k]['neant']=='false' and  'items' in i[k] and i[k]['items']!=None:
    			clean_entry[k]=i[k]['items']['items']
    			if len(i[k].keys())>2:
    				input('error, unusual file')
    	else:
    		clean_entry[k]=i[k]
    	print('----')
    result[key]=clean_entry
    if nom in last_result:
    	print('Dépôt existant')
    	if compare(i['dateDepot'],last_result[nom]['dateDepot']):
    		print('Dépôt plus récent')
    		last_result[nom]=clean_entry
    	else:
    		print('Dépôt plus ancien')
    else:
    	last_result[nom]=clean_entry

typesEffectif=collections.Counter(mandats)
print("Nb déclas base:",len(result.keys()),len(mandats)-1)
print("Types:",typesEffectif)

result = collections.OrderedDict(sorted(result.items()))
last_result = collections.OrderedDict(sorted(last_result.items()))

for k,v in result.items():
	print(k)
	printjs(v)
	print(v['mandat'])


dir='résultats - '+today+'/'
if os.path.exists(dir):
	shutil.rmtree(dir)
os.makedirs(dir)

if output_by_job:
	for t in typesEffectif.keys():
		print(t)
		with open(dir+"declarations-"+today+sampleStr+str(t)+".json", "w+") as jsonFile:
				jsonFile.seek(0)
				tresult={k:v for k,v in result.items() if v['mandat']==t or t=='tout'}
				json.dump(tresult, jsonFile, indent = 4, separators = (',', ':'))#, sort_keys=True)
				jsonFile.truncate()

	with open(dir+"dernieres-declarations-"+today+sampleStr+str(t)+".json", "w+") as jsonFile:
			jsonFile.seek(0)
			tresult={k:v for k,v in last_result.items() if v['mandat']==t or t=='tout'}
			json.dump(tresult, jsonFile, indent = 4, separators = (',', ':'))#, sort_keys=True)
			jsonFile.truncate()


if compute_diffs:
	print("Différences avec déclarations précédentes")
	results={}
	previous_name=''
	prev_decla={}
	for key in result.keys():
		print(key)
		name=key.split(' - ')[0]
		date=str(key.split(' - ')[1])
		decla=result[key]
		if name==previous_name:#compute diff
			print("compute diff...")
			difference=diff(prev_decla,decla,U=False)
			verbose("différence",printjs(difference))
			results[name]['MODIF - '+date]=difference
		else:
			results[name]={'INITIALE - '+date:decla,'mandat':decla['mandat']}
		prev_decla=decla
		previous_name=name



	for t in typesEffectif.keys():
		print(t)
		with open(dir+"declarations-diffs-"+today+sampleStr+str(t)+".json", "w+") as jsonFile:
				jsonFile.seek(0)
				tresult={k:v for k,v in results.items() if v['mandat']==t or t=='tout'}
				json.dump(tresult, jsonFile, indent = 4, separators = (',', ':'))#, sort_keys=True)
				jsonFile.truncate()
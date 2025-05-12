import json
from io import open
import sys

#lljkklkl
#recherche le mot cle  - 1er argument -  dans les fichiers demandes  - 2e et 3e argument -
#sans argument les fichiers sont les declarations et dernieres declarations dates d aujourd'hui (voir prgm "hatvp.py")

from datetime import date
today = str(date.today())

keyWords=[    "MORRIS",
		  "TOBACCO",
		  "JT INTERNATIONAL",
		  "SEITA",
		  "ALTRIA",
		  "BURALISTE",
		  "SOVAPE",
		  "FIVAPE",
		  "MARKO",
		  "TMA",
		  "IMAGE 7",
		  "PLEAD",
		  "FORWARD PARTNERS","FOWARD PARTNERS" ,
		  "REVA",
		  "RUDINGER",
		  "MARTEL",
		  "BRUQUEL",
		  "RANNOU",
		  "LEROUX",
		  "TIFRATENE",
		  "FRITSCH",
		  "MARBOIS", 
		  "CHARBONNEAU",
		  "ZAPPIA",
    "SCALES","LALO",
    "NATALI","MALLARD","CHELBANI"  ,
    "BENOIT BAS","SAUCE","RUDIGOZ","tabac",
    "Vapot",
    "Cigar"]#sys.argv[1]
keyWordStr='lobby-tabac'#keyWords[1]+' etc-'
keyWords=[k.lower() for k in keyWords]

filename= sys.argv[2] if len(sys.argv)>2 else 'declarations.json' #'résultats - '+today+'/declarations-'+today+'tout.json'

filename2= sys.argv[3] if len(sys.argv)>3 else 'dernieres-declarations.json'

print(str(keyWords),filename,filename2,today)

with open(filename, "r+") as jsonFile:
		obj = json.load(jsonFile)
with open(filename2, "r+") as jsonFile:
		last_obj = json.load(jsonFile)


exclude_field="base64EncodedContent"

results={}
def find(o,path):#find keyword in all declarations
	if isinstance(o,dict):
		for k in o.keys():
			#path+=[k]
			if k!=exclude_field:
				find(o[k],path+[k])
			#path.pop()
	elif isinstance(o,list):
		for i in o:
			#path+=['item']
			s='item'
			if 'nom' in i:
				s=i['nom']
			if 'general' in i:
				s=i['general']['declarant']['prenom']+' '+i['general']['declarant']['nom']
			find(i,path+[s])
	elif o:
		for kwd in keyWords:
			if kwd in o.lower():
				print('match',kwd,path,o)
				results[' >> '.join(path)]=";keyword: "+kwd+"; dans "+o


last_results={}
def find_last(o,path):#find keyword in last declarations of each
	if isinstance(o,dict):
		for k in o.keys():
			#path+=[k]
			if k!=exclude_field:
				find_last(o[k],path+[k])
			#path.pop()
	elif isinstance(o,list):
		for i in o:
			#path+=['item']
			s='item'
			if 'nom' in i:
				s=i['nom']
			if 'general' in i:
				s=i['general']['declarant']['prenom']+' '+i['general']['declarant']['nom']
			find_last(i,path+[s])
	elif o:
		for kwd in keyWords:
			if kwd in o.lower():
				print('match',kwd,path,o)
				last_results[' >> '.join(path)]=";keyword: "+kwd+"; dans "+o

print("search last entries?")
find_last(last_obj,[])

with open('résultats'+'/'+filename2+'-search-'+keyWordStr+"-"+today+".csv", "w+") as f:
	for k in last_results.keys():
		f.write(k+';'+last_results[k]+'\n')


input("search all entries?")

find(obj,[])

with open('résultats'+'/'+filename+'-search-'+keyWordStr+"-"+today+".csv", "w+") as f:
	for k in results.keys():
		f.write(k+','+results[k]+'\n')


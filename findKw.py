import json
from io import open
import sys

#lljkklkl
#recherche le mot cle  - 1er argument -  dans les fichiers demandes  - 2e et 3e argument -
#sans argument les fichiers sont les declarations et dernieres declarations dates d aujourd'hui (voir prgm "hatvp.py")

from datetime import date
today = str(date.today())

keyWord="vapot"#sys.argv[1]
filename= sys.argv[2] if len(sys.argv)>2 else 'résultats - '+today+'/declarations-'+today+'tout.json'

filename2= sys.argv[3] if len(sys.argv)>3 else 'résultats - '+today+'/dernieres-declarations-'+today+'tout.json'

print(keyWord,filename,filename2,today)

with open(filename, "r+") as jsonFile:
		obj = json.load(jsonFile)
with open(filename2, "r+") as jsonFile:
		last_obj = json.load(jsonFile)




results={}
def find(o,path):#find keyword in all declarations
	if isinstance(o,dict):
		for k in o.keys():
			#path+=[k]
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
		if keyWord in o.lower():
			print('match',path,o)
			results[' >> '.join(path)]=o


last_results={}
def find_last(o,path):#find keyword in last declarations of each
	if isinstance(o,dict):
		for k in o.keys():
			#path+=[k]
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
		if keyWord in o.lower():
			print('match',path,o)
			last_results[' >> '.join(path)]=o


find(obj,[])
find_last(last_obj,[])

with open(filename+'-search-'+keyWord+".csv", "w+") as f:
	for k in results.keys():
		print(k)
		f.write(k+','+results[k]+'\n')

with open(filename2+'-search-'+keyWord+".csv", "w+") as f:
	for k in last_results.keys():
		f.write(k+';'+last_results[k]+'\n')

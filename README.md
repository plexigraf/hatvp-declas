# hatvp-json
Le programme `hatvp.py` effectue trois opérations sur le fichier de déclarations disponible sur le site HATVP.fr à https://www.hatvp.fr/livraison/merge/declarations.xml:
 - Rangement par ordre alphabétique et chronologique des déclarations, conversion en `json` dans le fichiers `declarations-[date].json`
 - Génération du fichier `dernieres-declarations-[date].json` avec les déclarations les plus récentes de chaque déclarant
 - Génération du fichier `declarations-diffs-[date].json` recensant les modifications apportées par chaque déclarant à chaque nouvelle déclaration

## Syntaxe

La syntaxe est `hatvp.py [xml]` où l'argument `[xml]` est optionnel et doit contenir le nom du fichier des déclarations en xml téléchargé sur le site de la HATVP, par défaut le programme considère que ce nom est `declarations.xml`.

Les fichiers produits sont `declarations-[date].json`, `dernieres-declarations-[date].json`, `declarations-diff-[date].json`.

## Installation

Requiert Python 3 et les packages xml,json,xmltodict (Avec Python 2 les deux premiers fichiers sont générés, mais le fichier des différences est erroné).

## déclarations avec un mot-clé donné

La commande `findKW.py keyword [file1.json] [file2.json]` recherche le mot clé `keyword` à tous les niveaux des déclarations contenues dans les fichiers `file1.json` et `file2.json` produits par le programme `hatvp.py`. Par défaut, `file1` est `declarations-[date]` et `file2` est `dernieres-declarations-[date]`, de telle sorte à ce qu'on puisse faire tourner les deux programmes l'un après l'autre.

Les fichiers produits sont en format csv et son nommés `resultats-[file1]-search-[keyword].csv` et `resultats-[file2]-search-[keyword].csv`


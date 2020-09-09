# Description:
Projet de sauvegarde d'un/plusieurs site(s) web(s) fonctionnant sous Apache et MySQL:
- Sauvegarde automatisée de la base de données MYSQL ainsi que du site web contenu dans le dossier /var/www(configurable) avec exportation de la sauvegarde dans un dossier local dédié.
- Possibilité d'effectuer les sauvegardes par lot de plusieurs sites à l'aide du menu( à configurer dans le fichier yaml)
- possibilité de sauvegarde individuel à l'aide d'argument passé en ligne de commande

# Configuration:
 - Web serveur Debian 10, apache2, mysql-server.

# Développement:
Script Python crée Aout 2020, sur Debian 10 et python 2.7.16

# Prérequis:
- Installer pip
Pip est un système de gestion de paquets utilisé pour installer et gérer des librairies écrites en Python .
Pip empêche les installations partielles en annonçant toutes les exigences avant l'installation.
	Pour installer pip il vous faudra exécuter la commande :
	sudo apt-get install python-pip
	Et pour python 3 :
	sudo apt-get install python3-pip

- Installer YAML
YAML (YAML Ain't Markup Language) est un langage de sérialisation de données lisible par l'homme.
Il est couramment utilisé pour les fichiers de configuration.
YAML prend en charge nativement 3 types de données de base: les scalaires (tels que les chaînes, les entiers et les flottants), les listes et les tableaux associatifs.
L'extension de nom de fichier officielle recommandée pour les fichiers YAML a été .yaml.
Il existe deux modules en Python pour YAML: PyYAML et ruamel.yaml.

- Dans ce script, nous utilisons le module pyyaml
PyYAML est un analyseur et un émetteur YAML pour Python, le module est installé avec pip.
$ pip3 install pyyaml

- Script "backup.py"

- Disposer d'un user et mot de passe root MySQL pour la bdd et d'un user root sur la machine debian uniquement pour le choix(4) :la restauration site web

- Positionner dans le répertoire home le fichier yaml ".acces_db.yml"  et renseigner le fichier yaml(comme dans le fichier exemple ".acces_db.yml" mis à disposition) avant le lancement du script
 
# Utilisation:
- Renseigner les variables du fichier yaml en fonction des taches à automatiser pas de limite en nombre de site
- Des dossiers de backup de Database et Web sont créés automatiquement si inexistant

- le Script s'utilise selon 3 possibilié :
	- sans argument, en utilisant le menu -> # python3 backup.py /home/administrateur/.acces_db.yml
Le menu s'affiche de la manière suivante:

Veuillez saisir le numero correspondant a votre choix :

	[1] => Sauvegarder les bases mysql
	[2] => Restaurer les bases mysql
	[3] => Sauvegarder des sites web
	[4] => Restaurer des sites web(root)
	[5] => 

	[6] => Exit

	- en utilisant 1 argument (l'action de sauvegarde/restauration pour la bdd/www des sites présents dans le fichier yaml)
		-> ex: $ python3 backup.py /home/administrateur/.acces_db.yml 1 [1] => Sauvegardera les bases mysql de la liste de tous les sites présent dans le fichier yaml

	- en utilisant 2 arguments (action argument 1(sauvegarde/restauration bdd/www) + argument 2 définissant le nom du site souhaité)
		-> ex: $ python3 backup.py /home/administrateur/.acces_db.yml 3 site2 => Sauvegarder le site web uniquement pour le site2 uniquement

Les fichiers 
*.tar" (sauvegarde des fichiers du site web) sont sauvegardés sous la forme www_Nom Site_Date du Jour.tar dans le répertoire ~/sauvegarde_web
et *.sql" (sauvegarde de la base de données mysql) sous la forme DateduJourNomdeBase.sql dans le répertoire ~/sauvegarde_db

Ci-dessous les variables de définition dans le fichier de configuration yaml ".acces_db.yml":
	conf:
	  backup:
	    dossier_sauv: 
	    backup_dir_web: 

	sites:
	  siteN:
	    mysql:
	      host: localhost   #nom du host du siteN
	      user: root	#utilisateur root MySQL du siteN
	      passwd: 123456	#mot de passe du user MySQL du siteN
	      db: testN		#nom de la base de donnees MySQL du siteN
	   web:
      	      racine: /var/www  #répertoire www du siteN
     
# Les étapes du script:
 - importation des modules:
	import os
	import sys
	from os.path import expanduser
	import time
	import datetime
	import shutil
	import yaml
	import subprocess
 
 - Affectation de la date à une variable
	 TODAYDATE

- chargement_config(fichier_conf)
	Accès au fichier yaml

	DB_BACKUP = config['conf']['backup']['dossier_sauv']
	BACKUP_DIR_WEB = config['conf']['backup']['backup_dir_web']

- Execution du main avec config en paramètre et traitement des arguments passés à Backup.py
- Suivant l'action choisie :
	Sauvegarde de Bases de Donnees MySQL
	Recherche du répertoire de sauvegarde et création si inexistant

	Restauration des Bases de Donnees MySQL

	Sauvegarder de site web
	Recherche du répertoire de sauvegarde et création si inexistant
	Archivage  dans le dossier web de sauvegarde, au format tar, du dossier web situé dans /var/www (paramétrable dans le fichier de conf yaml)
	Restauration des Sites Web


Gestion des execeptions
$ echo $?
exit(0) -> tentavive execution du main
exit(1) -> pas de fichier yaml
exit(2) -> sortie menu
	
# LICENCE
"This project is licensed under the terms of the GPLv3 license."

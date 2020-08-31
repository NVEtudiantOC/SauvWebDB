# Description:
Projet de sauvegarde d'un/plusieurs site(s) web(s) fonctionnant sous Apache et MySQL:
- Sauvegarde automatisée de la base de données MYSQL ainsi que du site web contenu dans le dossier /var/www avec exportation de la sauvegarde dans un dossier local dédié.
- Possibilité d'effectuer les sauvegardes par lot de plusieurs sites ( à configurer dans le fichier yaml)

# Configuration:
 - Web serveur Debian 10, apache2, mysql-server.

# Développement:
Script Python crée Aout 2020, sur Debian 10 et de python version 2.7.16.

# Prérequis:
- Script "backup.py"
- Disposer d'un user et mot de passe root MySQL
- Positionné dans le répertoire home? le fichier yaml ".acces_db.yml"  et le complété avant lancement du script
 
# Utilisation:
- Renseigner les variables du fichier yaml en fonction des taches à automatiser
- Des dossiers de backup de Database et Web sont créés automatiquement

- le Script s'utilise selon 3 possibilié :
	- sans argument, en utilisant le menu -> $ python3 backup.py

Veuillez saisir le numero correspondant a votre choix :

	[1] => Sauvegarder les bases mysql
	[2] => Restaurer les bases mysql
	[3] => Sauvegarder des sites web
	[4] => Restaurer des sites web
	[5] => Sauvegarde Site Web et Base de Donnees MySQL

	[6] => Exit

	- en utilisant 1 argument (l'action de sauvegarde/restauration pour la bdd/www des sites présent dans le fichier yaml)
		-> ex: $ python3 backup.py 1 [1] => Sauvegardera les bases mysql de la liste de tous les sites

	- en utilisant 2 arguments (action argument 1(sauvegarde/restauration bdd/www) + argument 2 définissant le nom du site souhaité)
		-> ex: $ python3 backup.py 3 site2 => Sauvegarder le site web uniquement pour le site2

Les fichiers 
*.tar" (sauvegarde des fichiers du site web) sont sauvegardés sous la forme www_Nom Site_Date du Jour.tar
et *.sql" (sauvegarde de la base de données mysql) sous la forme DateduJourNomdeBase.sql


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

 - Affectation de la localisation des fichiers de fonctionnement
	 fichier_conf = home + "/.acces_db.yml"

- chargement_config(fichier_conf)

	 DB_BACKUP = config['conf']['backup']['dossier_sauv']
	 BACKUP_DIR_WEB = config['conf']['backup']['backup_dir_web']

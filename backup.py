#!/usr/bin/python3.7.3
# -*-coding:utf-8 -*

import os
import sys
from os.path import expanduser
import time
import datetime
import shutil
import yaml
import subprocess
import tarfile

TODAYDATE = time.strftime('%Y%m%d')

 ##### Fonctions ####

def efface_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def chargement_config(fichier_conf):
	content = {}
	if not os.path.exists(fichier_conf):
		print("Fichier" + fichier_conf + " non trouve")
		exit(1)
	else:
		with open(fichier_conf, 'r') as ymlfile:
			content = yaml.load(ymlfile, Loader=yaml.BaseLoader)
			return content

##### Fonctions sauvegarde et restauration bdd ####

def sauvegarde_db(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,TODAYDATE):
    serveur_sauv = config['conf']['backup']['ip_sauv_dist']
    print ("Debut de la sauvegarde de la base de donnees " + DB_NAME)
    fichier_sauvegarde = str(DB_BACKUP) + TODAYDATE + DB_NAME
    #dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + str(DB_PASSWORD) + " " + DB_NAME + ' > ' + fichier_sauvegarde + ".sql"
    dumpfile = fichier_sauvegarde + ".sql"
    upfile_db = dumpfile + ".gz"
    tmpfile = open(dumpfile,'w')
    try:
    	subprocess.run(["mysqldump","--host=" + DB_HOST, "--user=" + DB_USER, "--password=" + str(DB_PASSWORD), DB_NAME], stdout=tmpfile)
    	tmpfile.close()
    	subprocess.run(["gzip", dumpfile])
    except subprocess.CalledProcessError as e: #Classe de base pour toutes les subprocessexceptions
    	print('erreur rencontrée lors de la sauvegarde de la base de données',e.output)
    #gzipcmd = "gzip " + fichier_sauvegarde + ".sql"
    print ("Sauvegarde terminée\n")
    print ("La sauvegarde a été créée dans le fichier '" + fichier_sauvegarde + ".sql.gz'\n")
    #subprocess.run(["scp", upfile_db, "administrateur@192.168.0.3:~/sauvegarde_db"])
    #subprocess.run(["scp", upfile_db, DB_USER + "@192.168.0.3:" + DB_BACKUP])
    subprocess.run(["scp", upfile_db, DB_USER + "@" + str(serveur_sauv) +":" + DB_BACKUP])
    return(0)


def restaure_db(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,TODAYDATE) -> None:
	for delta in range(8):
		TODAYDATE = datetime.date.today()-datetime.timedelta(delta)
		sauvegarde = str(DB_BACKUP) + str(TODAYDATE.strftime('%Y%m%d')) + DB_NAME + ".sql.gz"
		if os.path.exists(sauvegarde):
			print("Une sauvegarde située dans'" + DB_BACKUP + "' a été trouvé!")
			print ("La sauvegarde la plus récente est : '" + sauvegarde + "'")
			try:
				gunzip = subprocess.Popen(['gunzip', '-c', sauvegarde], stdout=subprocess.PIPE)
				mysqlcmd = ['mysql', '-u', DB_USER, '-p' + str(DB_PASSWORD), '-h', DB_HOST, DB_NAME]
				process = subprocess.Popen(mysqlcmd, stdin=gunzip.stdout)
				process.wait()				
				print("La sauvegarde '" + sauvegarde + "' a été restaurée avec succes!\n")
				break
				print("Restauration terminée!")
			except subprocess.CalledProcessError as e: #Classe de base pour toutes les subprocessexceptions
				print('erreur rencontrée lors de la sauvegarde de la base de données',e.output)			
		else:
			print ("Fichier de sauvegarde '" + sauvegarde + "'à J-" + str(delta) + " n'existe pas!...")

##### Fonctions sauvegarde et restauration www ####

def sauvegarde_www(site,key,TODAYDATE) -> None:
	serveur_sauv = config['conf']['backup']['ip_sauv_dist']
	USER = site['sites'][key]['mysql']['user']
	print("Compression du dossier web  (/var/www...) du " + str(key) + "...")
	fichier_sauvegarde = str(BACKUP_DIR_WEB) + '/www' + '_' + str(key) + '_' + TODAYDATE + '.tar'
	dossier_racine = site['sites'][key]['web']['racine']
	#os.system('tar --absolute-names -czf '+ config['conf']['backup']['backup_dir_web'] + '/www' + '_' + str(key) + '_' + TODAYDATE +'.tar ' + site['sites'][key]['web']['racine'])
	try:
		print("Compression du dossier: ", dossier_racine)
		dossier_tar = tarfile.open(fichier_sauvegarde, 'w')
		dossier_tar.add(dossier_racine)
		dossier_tar.close()
		#os.system('tar -cf '+ fichier_sauvegarde + site['sites'][key]['web']['racine'])
		#os.system('tar -cf '+ config['conf']['backup']['backup_dir_web'] + str(key) + '_' + TODAYDATE +'.tar ' + site['sites'][key]['web']['racine'])
		print("La sauvegarde de '" + dossier_racine + "' a été effectuée avec succès dans '" + fichier_sauvegarde + "'")
		#subprocess.run(["scp", fichier_sauvegarde, "administrateur@192.168.0.3:~/sauvegarde_web"])
		subprocess.run(["scp", fichier_sauvegarde, str(USER) + "@" + str(serveur_sauv) +":" + BACKUP_DIR_WEB])
		print ("Sauvegarde du Site Web " + fichier_sauvegarde + " sur serveur distant, éffectuée!")
	except tarfile.TarError as e: #Classe de base pour toutes les tarfileexceptions
		print('Erreur rencontrée lors de la sauvegarde des fichiers du site Web',e)

def restaure_www(site,key,TODAYDATE) -> None:
	for delta in range(8):
		TODAYDATE = datetime.date.today()-datetime.timedelta(delta)
		fichier_sauvegarde = str(BACKUP_DIR_WEB) + '/www' + '_' + str(key) + '_' + str(TODAYDATE.strftime('%Y%m%d')) + ".tar"
		if os.path.exists(fichier_sauvegarde):
			try:
				dossier_tar = tarfile.open(fichier_sauvegarde)
				dossier_racine = site['sites'][key]['web']['racine']
				print("Une sauvegarde située dans'" + BACKUP_DIR_WEB + "' a été trouvé!")
				print ("La sauvegarde la plus récente est : '" + fichier_sauvegarde + "'")
				#print("Restauration du site: " + site['sites'][key]['web']['racine'])
				print("Restauration du site: ", dossier_racine)
				dossier_tar.extractall('/')
				#dossier_tar.extractall('/var/www')
				#dossier_tar.extractall(BACKUP_DIR_WEB)
				dossier_tar.close()
				print("La sauvegarde '" + fichier_sauvegarde + "' a été restaurée avec succes!")
			except tarfile.TarError as e: #Classe de base pour toutes les tarfileexceptions
				print('Erreur rencontrée lors de la restauration des fichiers du site Web',e)
			break
			print("Restauration terminée!")
		else:
			print ("Fichier de sauvegarde '" + fichier_sauvegarde + "'à J-" + str(delta) + " n'existe pas!...")

def purge_backup(config):
	DB_BACKUP = config['conf']['backup']['dossier_sauv']
	BACKUP_DIR_WEB = config['conf']['backup']['backup_dir_web']
	retention = config['conf']['backup']['retention']
	# Supprimer les anciens fichiers .sql.gz et garder les n plus récents
	#DB_BACKUP = '/home/administrateur/sauvegarde_db/'
	nombre_fichier_recent = int(retention)
	#nombre_fichier_recent = 7
	#nombre_fichier_recent = config['backup']['retention']
	print("Dans le répertoire'" + DB_BACKUP + "'")
	print("Et dans le répertoire'" + BACKUP_DIR_WEB + "'")
	print("Uniquement '" + str(nombre_fichier_recent) + "' sauvegardes seront gardées!\n") 
	os.chdir(DB_BACKUP)
	fichiers = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
	fichiers_dat = []
	for element in fichiers:
	    if element.endswith('.sql.gz'):
	        fichiers_dat.append(element)
	#print("Contenu de fichiers_dat:'" + str(fichiers_dat) + "'\n")

	liste_nouveau = fichiers_dat[-nombre_fichier_recent:]
	#print("Contenu de liste_nouveau:'" + str(liste_nouveau) + "'\n") 

	file_to_delete = fichiers_dat
	#print("Contenu de file_to_delete:'" + str(file_to_delete) + "'\n")

	for r in liste_nouveau:
	    file_to_delete.remove(r)
	if file_to_delete:
	    for i in file_to_delete:
	        os.remove("{}".format(DB_BACKUP + '/' + i))
	# Supprimer les anciens fichiers .tar et garde les n plus récents
	#DB_BACKUP = '/home/administrateur/sauvegarde_db/'
	os.chdir(BACKUP_DIR_WEB)
	fichiers = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
	fichiers_dat = []
	for element in fichiers:
	    if element.endswith('.tar'):
	        fichiers_dat.append(element)
	#print("Contenu de fichiers_dat:'" + str(fichiers_dat) + "'\n")

	liste_nouveau = fichiers_dat[-nombre_fichier_recent:]
	#print("Contenu de liste_nouveau:'" + str(liste_nouveau) + "'\n") 

	file_to_delete = fichiers_dat
	#print("Contenu de file_to_delete:'" + str(file_to_delete) + "'\n")

	for r in liste_nouveau:
	    file_to_delete.remove(r)
	if file_to_delete:
	    for i in file_to_delete:
	        os.remove("{}".format(BACKUP_DIR_WEB + '/' + i))

##### Fonction gestion de l'action demandée par l'utilisateur ####

def action_choisie(choix, conf_backup, site) -> None:
    efface_console()
    config = conf_backup
    print("Clés dontenues dans le dictionnaire: ", site['sites'].keys())
    for key in site['sites'].keys():
      print("\nLa clé " + str(key) + " contient: ", site['sites'][key])
      #print(site['sites'][key])
      if choix == 1:
        print("\nMenu > Sauvegarde de Bases de Donnees MySQL\n")
        if os.path.exists(DB_BACKUP):
        	print("Dossier de Sauvegarde des Bases", DB_BACKUP , "trouvé!\n")
        else:
        	os.mkdir(DB_BACKUP)
        	print("Dossier de Sauvegarde des Bases", DB_BACKUP , "créé!")

        print("Sauvegarde de la Base de Donnees: ", site['sites'][key]['mysql']['db'])
        sauvegarde_db(site['sites'][key]['mysql']['host'],site['sites'][key]['mysql']['user'],site['sites'][key]['mysql']['passwd'],site['sites'][key]['mysql']['db'],TODAYDATE)

      elif choix == 2:
        print("Menu > Restauration des Bases de Donnees MySQL\n")
        print("Restauration de la Base de Donnees: ", site['sites'][key]['mysql']['db'], "(à 7 jours max)")
        restaure_db(site['sites'][key]['mysql']['host'],site['sites'][key]['mysql']['user'],site['sites'][key]['mysql']['passwd'],site['sites'][key]['mysql']['db'],TODAYDATE)
        print("Restauration terminée!")

      elif choix == 3:
        print("\nMenu > Sauvegarder de site web\n")
        if os.path.exists(BACKUP_DIR_WEB):
        	print("Dossier de Sauvegarde des Sites Web", BACKUP_DIR_WEB , "trouvé!")
        else:
        	os.mkdir(BACKUP_DIR_WEB)
        	print("Dossier de Sauvegarde des Sites Web", BACKUP_DIR_WEB , "créé!")

        print("Sauvegarde du : " + str(key))
        print("Situé dans: ", site['sites'][key]['web']['racine'])
        sauvegarde_www(site,key,TODAYDATE)
        print("Sauvegarde terminée!\n")

      elif choix == 4:
        print("Menu > Restauration des Sites Web(root)\n")
        #print("Restauration du site: " + site['sites'][key]['web']['racine'])
        print("Restauration du site (à 7 jours max): " + str(key))
        restaure_www(site,key,TODAYDATE)
        print("Restauration terminée!\n")

      elif choix == 5:
        print("Menu > Purge des Sauvegardes\n")
        purge_backup(config)
        print("Purge des Sauvegardes terminée!\n")
        
      elif choix == 6:
        exit(2)
      else:
        menu()

def menu(config):
    conf_backup = config
    print("Gestion de backup sites web (Web + Base de donnees).\n")
    print("Veuillez saisir le numero correspondant a votre choix :\n")
    print("\n\t[1] => Sauvegarder les bases mysql")
    print("\t[2] => Restaurer les bases mysql")
    print("\t[3] => Sauvegarder des sites web")
    print("\t[4] => Restaurer des sites web(root)")
    print("\t[5] => Purger les Sauvegardes")
    print("\n\t[6] => Exit")
    while True:
        try:
            choix = int(input("\n\nEntrez votre choix :\n > "))
            break
        except ValueError:
            sys.stderr.write("{}\nErreur: choix non défini\n\n{}")
    action_choisie(choix, conf_backup, conf_backup)


##### MAIN ####

def main(config):
    conf_backup = config

    print ("Nom du script: ", sys.argv[0])
    print ("Nombre d arguments: ", len(sys.argv))
    print ("Les arguments sont: " , str(sys.argv))

    if len(sys.argv) == 3:
        choix = int(sys.argv[2])
        
        if choix > 0 and choix < 6:
            action_choisie(choix, conf_backup, conf_backup)

    if len(sys.argv) == 4:
        choix = int(sys.argv[2])
        choix2 = str(sys.argv[3])
        
        site = {}
        site['sites'] = {}
        site['sites'][choix2] = conf_backup['sites'][choix2]
        
        if choix > 0 and choix < 6:
            action_choisie(choix,conf_backup, site)

    else:
        menu(conf_backup)


home = expanduser("~")
#fichier_conf = home + "/.acces_db.yml"
if len(sys.argv) >= 2:
    fichier_conf = sys.argv[1]
else:
	print("Pas de fichier de configuration fourni, arrêt du script")
	exit(1)

efface_console()
config = chargement_config(fichier_conf)

DB_BACKUP = config['conf']['backup']['dossier_sauv']
BACKUP_DIR_WEB = config['conf']['backup']['backup_dir_web']

if DB_BACKUP[-1:] != "/":
    DB_BACKUP = DB_BACKUP + "/"

try:
    main(config)
except KeyboardInterrupt:
    print('\nProcessus interrompu')
    try:
        sys.exit(0)
    except SystemExit:
        sys.exit(0)

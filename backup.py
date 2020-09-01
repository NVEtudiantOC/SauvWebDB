#!/usr/bin/python3
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

def efface_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def chargement_config(fichier_conf):
	content = {}
	if not os.path.exists(fichier_conf):
		print("Fichier" + fichier_conf + " non trouve")
		exit(1)
	else:
		with open(fichier_conf, 'r') as ymlfile:
			content = yaml.load(ymlfile)
			return content

def sauvegarde_db(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,TODAYDATE):
    print ("Debut de la sauvegarde de la base de donnees " + DB_NAME)
    fichier_sauvegarde = str(DB_BACKUP) + TODAYDATE + DB_NAME
    dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + str(DB_PASSWORD) + " " + DB_NAME + ' > ' + fichier_sauvegarde + ".sql"
    os.system(dumpcmd)
    gzipcmd = "gzip " + fichier_sauvegarde + ".sql"
    os.system(gzipcmd)
    print ("Sauvegarde terminée\n")
    print ("La sauvegarde a été créée dans le fichier '" + fichier_sauvegarde + ".sql.gz'")
    return(0)

def restaure_db(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,TODAYDATE) -> None:
    fichier_sauvegarde = str(DB_BACKUP) + TODAYDATE + DB_NAME + ".sql"
    unzip = subprocess.Popen(['gzip', '-d', fichier_sauvegarde], stdout=subprocess.PIPE)

    mysqlcmd = ['mysql', '-u', DB_USER, '-p' + str(DB_PASSWORD), '-h', DB_HOST, DB_NAME]

    process = subprocess.Popen(mysqlcmd, stdin=unzip.stdout)
    process.wait()

    print("La sauvegarde '" + fichier_sauvegarde + ".gz' a été restaurée avec succes")

def restaure_www(site,key,TODAYDATE) -> None:
    for delta in range(5):
            TODAYDATE = datetime.date.today()-datetime.timedelta(delta)
            fichier_sauvegarde = str(BACKUP_DIR_WEB) + '/www' + '_' + str(key) + '_' + TODAYDATE.strftime('%Y%m%d') + ".tar"
            if (os.path.exists(fichier_sauvegarde)):
                print("La sauvegarde située dans'" + fichier_sauvegarde + "' a été trouvé")
                dossier_tar = tarfile.open(fichier_sauvegarde)
                dossier_racine = site['sites'][key]['web']['racine']
                #print("Restauration du site: " + site['sites'][key]['web']['racine'])
                print("Restauration du site: ", dossier_racine)
                #Problème accès root
                dossier_tar.extractall(dossier_racine)
                #dossier_tar.extractall('/var/www')
                #dossier_tar.extractall(BACKUP_DIR_WEB)
                dossier_tar.close()
                print("La sauvegarde '" + fichier_sauvegarde + "' a été restaurée avec succes")

def action_choisie(choix, conf_backup, site) -> None:
    efface_console()
    config = conf_backup
    print("Clés dontenues dans le dictionnaire: ", site['sites'].keys())
    for key in site['sites'].keys():
      print("La clé " + str(key) + " contient: ", site['sites'][key])
      #print(site['sites'][key])
      if choix == 1:
        print("\nMenu > Sauvegarde de Bases de Donnees MySQL\n")
        if os.path.exists(DB_BACKUP):
        	print("Dossier de Sauvegarde des Bases", DB_BACKUP , "trouvé!\n")
        else:
        	os.mkdir(DB_BACKUP)
        	print("Dossier de Sauvegarde des Bases", DB_BACKUP , "créé")

        print("Sauvegarde de la Base de Donnees: ", site['sites'][key]['mysql']['db'])
        print("\n")
        sauvegarde_db(site['sites'][key]['mysql']['host'],site['sites'][key]['mysql']['user'],site['sites'][key]['mysql']['passwd'],site['sites'][key]['mysql']['db'],TODAYDATE)

      elif choix == 2:
        print("Menu > Restauration des Bases de Donnees MySQL\n")
        print("Restauration de la Base de Donnees: ", site['sites'][key]['mysql']['db'])
        restaure_db(site['sites'][key]['mysql']['host'],site['sites'][key]['mysql']['user'],site['sites'][key]['mysql']['passwd'],site['sites'][key]['mysql']['db'],TODAYDATE)
        print("Restauration terminée!")

      elif choix == 3:
        print("Menu > Sauvegarder de site web\n")
        if os.path.exists(BACKUP_DIR_WEB):
        	print("Dossier de Sauvegarde des Sites Web", BACKUP_DIR_WEB , "trouvé")
        else:
        	os.mkdir(BACKUP_DIR_WEB)
        	print("Dossier de Sauvegarde des Sites Web", BACKUP_DIR_WEB , "créé")

        try:
            print("Compression du dossier web  (/var/www...) du " + str(key) + "...")
            os.system('tar -cf '+ config['conf']['backup']['backup_dir_web'] + '/www' + '_' + str(key) + '_' + TODAYDATE +'.tar ' + site['sites'][key]['web']['racine'])
        except OSError as e:
            print('erreur rencontree avec les fichiers des sites Web',e)

      elif choix == 4:
        print("Menu > Restauration des Sites Web\n")
        print("Restauration du site: " + site['sites'][key]['web']['racine'])
        restaure_www(site,key,TODAYDATE)
        print("Restauration terminée!")

      elif choix == 5:
        print("Menu > Sauvegarde Site Web et Base de Donnees MySQL\n")
        print("Sauvegarde Base de Donnees MySQL en cours...\n")
        sauvegarde_db(site['sites'][key]['mysql']['host'],site['sites'][key]['mysql']['user'],site['sites'][key]['mysql']['passwd'],site['sites'][key]['mysql']['db'],TODAYDATE)
        print("\n")
        print("Sauvegarde Site web en cours...\n")
        try:
            print("Compression du dossier web du " + str(key) + " /var/www ...")
            os.system('tar -cf '+ config['conf']['backup']['backup_dir_web'] + '/www' + '_' + str(key) + '_' + TODAYDATE +'.tar ' + site['sites'][key]['web']['racine'])
        except OSError as e:
            print('erreur rencontree avec les fichiers des sites Web',e)
      elif choix == 6:
        exit(0)
      else:
        menu()

def menu(config):
    conf_backup = config
    print("Gestion de backup sites web (Web + Base de donnees).\n")
    print("Veuillez saisir le numero correspondant a votre choix :\n")
    print("\n\t[1] => Sauvegarder les bases mysql")
    print("\t[2] => Restaurer les bases mysql")
    print("\t[3] => Sauvegarder des sites web")
    print("\t[4] => Restaurer des sites web")
    print("\t[5] => Sauvegarde Site Web et Base de Donnees MySQL")
    print("\n\t[6] => Exit")
    while True:
        try:
            choix = int(input("\n\nEntrez votre choix :\n > "))
            break
        except ValueError:
            sys.stderr.write("{}\nErreur: choix non défini\n\n{}")
    action_choisie(choix, conf_backup, conf_backup)

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
	print("pas de fichier de config fourni, arrt du script")
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

# SauvWebDB
Projet de sauvegarde d'un/plusieurs site(s) web(s) fonctionnant sous Apache et MySQL

# Description:
Projet de sauvegarde d'un/plusieurs site(s) web(s) fonctionnant sous Apache et MySQL:
- Sauvegarde automatisée de la base de données MYSQL ainsi que du site web contenu dans le dossier /var/www avec exportation de la sauvegarde dans un dossier local.
- Possibilité d'effectuer les sauvegardes par lot de sites ( à configurer dans le fichier yaml)

# Configuration:
 - Web serveur Debian 10, apache2, mysql-server.


# Développement:
Script Python crée Aout 2020, sur une machine Debian version 10 et de python version 2.7.16.

# Prérequis:
- Script "backup.py"
- Disposer d'un user et mot de passe root MySQL

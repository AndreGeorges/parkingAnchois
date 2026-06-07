 ***Le but du projet*** 
 
 Développer un système de gestion de parking automatique intelligent à l'aide d'un Raspberry Pi, de capteurs et d'interfaces graphiques. 
 Le système permet de contrôler l'entrée et la sortie des véhicules, de gérer les places disponibles et d'envoyer des rappels a l'usager quand son temps d'expiration approche. 
 Ce projet met en pratique les notions vues dans le cours de programmation embarquée, notamment la gestion des GPIO, les interfaces graphiques, les API Web, les fichiers de configuration et l'architecture logicielle modulaire.

 ***Les fonctionnalités principales*** 
 
• action à l’entrée et à la sortie des vehicules ;  
• machine à états pour gerer l'entree, la sortie, le paiement, etat idle ou ferme, annulation ;  
• interface PyGame: on voit le nb de places disponibles, le tarif, changement de couleur selon l'etat;  
• boutons avec GPIO, LEDs, buzzer, servomoteur ;  
• affichage de la météo OpenWeatherMap, sauvegarde des icones localement et icone par defaut en cas de mauvaise connection ;  
• envoi de courriels SMTP;  
• journalisation des événements dans un fichier de log et export de log par pygame;  
• Interface d'authentification tkinter gerant les ouvertures/fermetures ainsi que la sortie du mode erreur.  



 ***Les nouvelles fonctionnalités du projet final*** 
 
 • fichier de configuration YAML qui controle certains parametres: code secret, API...;
 • interface tkinter avec clavier pour entrer password pour passer a etat super admin;
 • ajout de 3 etats: utilisateur, admin, superadmin;      
 • telechargement local des icones meteo et icone par defaut si impossible de charger;      



 ***La structure des dossiers*** 
.
├── assets
│   ├── images
│   │   └── fond.jpg
│   └── __init__.py
├── config
│   ├── config_loader.py                    *** ancien config.py
│   ├── __init__.py
│   └── ui_config.py                        ***  get_tarif() get_screen_color() get_color()
├── config.yaml
├── controllers
│   ├── email_controller.py                 *** ancien comm.py (logique email)
│   ├── gpio_controller.py                  *** ancien gpio_manager.py
│   ├── __init__.py
│   ├── parking_controller.py               *** ancien crud.py
│   └── state_controller.py                 *** eviter_surcharge_...
├── data
│   ├── db.json
│   └── transactions.json
├── Diagramme_etat_stationnement.png
├── exports
│   └── __init__.py
├── logs
│   ├── __init__.py
│   └── parking.log
├── main.py
├── models
│   ├── __init__.py
│   ├── logger_manager.py                               *** ancien logsconfig.py
│   ├── parking.py                                      *** ancien shared_state.py
│   ├── state_machine.py                                *** ancien etats.py
│   └── vehicle.py                                      *** ancien liste_vehicules.py

├── README.md
├── services
│   ├── email_service.py                            *** ancien comm.py (SMTP / envoi email)
│   ├── __init__.py
│   └── weather_service.py                          *** ancien api.py
└── views
    ├── pygame_view.py                              *** ancien ui_pygame.py
    └── tkinter_auth_view.py                        *** ancien ui_tkinter.py

17 directories, 63 files


utils:
def eviter_surcharge_etat()
def eviter_surcharge_event()      --->   controllers/state_controller.py

get_tarif()
get_AUTH()
get_screen_color()
get_color()                     ---->   config/ui_config.py

draw_keyboard()
draw_button()
bouton_journal()                ---->  views/pygame_view.py



 
 ***Le rôle de chaque module*** 

 main.py
 - Démarre les différents modules, fait fonctionner la machine a etat et répond aux différentes interactions

 config.yaml
 - Fichier contenant les configurations nécessaires pour changer les parametres de notre programme sans tout re-programmer

 config_loader.py
 - Va piger dans le fichier YAML

 ui_config.py
 - Retourne certaines informations du Fichier YAML en passant par config_loader

 gpio_controller.py
- envoie les informations au Raspberry pi pour controller les différentes composantes physique du stationnement

 parking_controller.py
 - Gere les vehicules qui entrent et sortent du stationnement

 state_controller.py
 - fonctions qui evite au logging de se repeter
 db.json
 - Fichier contenant les vehicules present dans le stationnement ainsi que les informations necessaires reliés à celui ci

 transactions.json
 - Fichier contenant l'historique des transactions s'étant déroulé dans le stationnement

 export_journal.py
 - fonction qui export les le fichier de log et crée un nouveau fichier vide

 logger_manager.py
 - Fichier qui gère ce qui sera ajouté dans le fichier de log

 parking.py
 - sert à faire le pont entre les informations utilisés par différents modules tel que main, tkinter_auth_view et  pygame_view

 state_machine.py
 - Contient les énumerations des etats et des evenements
 
 vehicle.py
 - Fichier qui gere la liste de vehicule et les informations ratachés à ceux ci

 email_service.py
 - Fichier qui gere l'envoi de courriels.  

 weather_service.py
 - Fichier qui va chercher les informations meteo ainsi que l'heure affiché

 tkinter_auth_view.py
 - Fichier qui gere l'écran d'authentification lorsque nécessaire
 
 pygame_view.py
 - Fichier qui gere l'affichage de l'ecran principale

 
 ***La configuration du fichier yaml*** 

	parking ---------- Contient la capacite maximale du stationnement
	security  ---------- Contient les informations relié à l'authentification par tkinter
	openweathermap ---------- Contient les informations de connection a l'API
	TARIFS ---------- la relation duree/tarif
	COLOR ---------- Banque de couleur RGB
	SCREEN_COLOR ---------- choix de couleurs selon l'etat
	BOUTONS_PHYSIQUES ---------- liste des boutons physique affiché
	gpio ---------- Contient le numeros des pins reliés aux composantes physiques
	durations ---------- Contient les durations possible
	journal ---------- Contient des informations pour la journalisation
	auth_view ---------- Contient les informations de configurations de la fenetre tkinter

 
 ***Les étapes d’installation*** 
 
 Pour l'installation des bibliothèques nécessaires:

 pip install -r requirement.txt

 ***Les bibliothèques nécessaires***

 Bibliotheques deja installés dans python :

	time 
	datetime 
	threading
	io
	os
	json
	logging
	smtplib
	enum 
	tkinter 

Bibliotheque à installer :

	pygame
	requests
	yaml
	gpiozero


 **La procédure de lancement** 

 Lancer le programme à partir du main.py
 
 ***Les problèmes connus ou limites du projet*** 



********************  NOTES SUR LE DIAGRAMME D'ETAT **************

''`

Le nombre de tentatives doit être initialisé à 0
Le système tombe en erreur;
le btn 7 ouvre la fenêtre tkinter ou on demande d’entrer le mot de passe
en dessous de 3 tentatives, on boucle entre les état USER_PASSWD ( or whatever you want to call it ) et ERREUR;
	( chaque tentative incorrecte nous ramène à ERREUR )
	La tentative successful nous amène à l’état IDLE
au-dessus de 3 tentatives, on boucle entre entre les états SUPERADMIN et ERREUR; 
	( chaque tentative incorrecte nous ramène à ERREUR )
	La tentative successful nous amène à l’état IDLE
	Ce qui détermine qu’on reste dans cette boucle-là, c’est le nb des tentatives qui est au-dessus de 3. Voilà pourquoi il fallait l’initialiser à 0 AVANT de rentrer dans l’état ERREUR
`
 ***Le but du projet*** 
 
 Développer un système de gestion de parking automatique intelligent à l'aide d'un Raspberry Pi, de capteurs et d'interfaces graphiques. 
 Le système permet de contrôler l'entrée et la sortie des véhicules, de gérer les places disponibles et d'envoyer des rappels a l'usager quand son temps d'expiration approche. 
 Ce projet met en pratique les notions vues dans le cours de programmation embarquée, notamment la gestion des GPIO, les interfaces graphiques, les API Web, les fichiers de configuration et l'architecture logicielle modulaire.

 ***Les fonctionnalités principales*** 
 
• action à l’entrée et à la sortie des vehicules ;  
• machine à états pour gerer l'entree, la sortie, le paiement, etat idle ou ferme, annulation ;  
• interface PyGame: on voit le nb de places disponibles, le tarif, changement de couleur selon l'etat;  
• boutons avec GPIO, LEDs, buzzer, servomoteur ;  
• affichage de la météo OpenWeatherMap ;  
• envoi de courriels SMTP;  
• journalisation des événements dans un fichier de log.  


 ***Les nouvelles fonctionnalités du projet final*** 
 
 • fichier de configuration YAML qui controle certains parametres: code secret, API...;
 • interface tkinter avec clavier pour entrer password pour passer a etat super admin;
 • ajout de 3 etats: utilisateur, admin, superadmin;      


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
get_screen_color()
get_color()                     ---->   config/ui_config.py

draw_keyboard()
draw_button()
bouton_accueil()                ---->  views/pygame_view.py



 
 ***Le rôle de chaque module*** 
 
 ***La configuration du fichier yaml*** 
 
 ***Les étapes d’installation*** 
 
 ***Les bibliothèques nécessaires***
 
 **La procédure de lancement** 
 
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
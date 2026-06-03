import yaml

with open("config.yaml", "r") as y:
    CONFIG = yaml.safe_load(y)

TARIFS = CONFIG["TARIFS"]

# pour openweathermap
API_KEY = CONFIG["API_KEY"]
city = CONFIG["city"]
lang = CONFIG["lang"]

# garder ici les informations sensibles, comme les emails, passwords, cle API, etc
sender_email = 'info.lpleboeuf@gmail.com'
recipient_email = 'info.lpleboeuf@gmail.com'
app_password ='xtmo gtar lvrb hdcq'


# sont appeles dans le pygame
COLOR = CONFIG["COLOR"]
# COLOR = {
#     "BLUE" : (10,29,121),
#     "WHITE" : (216, 229, 253),
#     "BLACK" : (50,50,50),
#     "VERT" : (135,238,169),
#     "VERT_POMME" : (128, 255, 0),
#     "JAUNE" : (230, 249, 138),
#     "ORANGE" : (243,133,78),
#     "GRIS" : (160, 160, 160),
#     "VIOLET" : (153, 51, 255),
#     "ROUGE" : (255,0,0),
#     "BRUN" : (153,0,0)
# }

# sont appeles dans le pygame pour affichage
SCREEN_COLOR = {
    "IDLE" : COLOR["VERT"],
    "ATTENTE ENTREE": COLOR["JAUNE"],
    "PAIEMENT ENTREE": COLOR["ORANGE"],
    "ACCES ACCEPTE" : COLOR["VERT_POMME"],
    "STATIONNEMENT" : COLOR["GRIS"],
    "ATTENTE SORTIE" : COLOR["VIOLET"],
    "ERREUR" : COLOR["ROUGE"],
    "FERME" : COLOR["BRUN"]
}
# sont appeles dans le pygame pour affichage
BOUTONS_PHYSIQUES = {
    1: "detecte vehicule entree",
    2: "selection duree",
    3: "confirmer paiement",
    4: "detecte vehicule sortie",
    5: "annulation",
    6: "declencher erreur",
    7: "passage erreur-idle",
    8: "toggle idle-ferme"
}

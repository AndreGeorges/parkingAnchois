import yaml

with open("config.yaml", "r") as y:
    CONFIG = yaml.safe_load(y)

TARIFS = CONFIG["TARIFS"]

# pour openweathermap
OPENWEATHER = CONFIG["openweathermap"]
# API_KEY = CONFIG["API_KEY"]
# city = CONFIG["city"]
# lang = CONFIG["lang"]

# garder ici les informations sensibles, comme les emails, passwords, cle API, etc
# email = CONFIG["email"]
sender_email = CONFIG["sender_email"]
recipient_email = CONFIG["recipient_email"]
app_password = CONFIG["app_password"]


# sont appeles dans le pygame
COLOR = CONFIG["COLOR"]

# sont appeles dans le pygame pour affichage
SCREEN_COLOR = {
    etat: COLOR[nom_couleur]
    for etat, nom_couleur in CONFIG["SCREEN_COLOR"].items()
    }

# sont appeles dans le pygame pour affichage
BOUTONS_PHYSIQUES = CONFIG["BOUTONS_PHYSIQUES"]

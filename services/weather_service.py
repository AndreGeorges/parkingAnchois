import io
import requests
import pygame
from config.logsconfig import logapi
from config.config_loader import API_KEY, city, lang
# import yaml

# with open("config.yaml", "r", encoding="utf-8") as file:
#     config = yaml.safe_load(file)
    
# city = config["city"]
# lang = config["lang"]
# API_KEY = config["API_KEY"]

# cette fonction appelle openweathermap . elle est importee dans ui_pygame
def get_weather():
    try:  #pour vérifier et logger les Erreurs
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}"        # definie dans config.py
            f"&appid={API_KEY}"        # la cle se trouve dans config.py comme le veut la pratique de cacher les infos sensibles
            f"&units=metric"
            f"&lang={lang}"  # definie dans config.py
        )

        response = requests.get(url,timeout=5) # timeout donne 5 secondes max pour se connecter
        response.raise_for_status() #s'assure que l'API est  connecté sinon erreur
        data = response.json()

        
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        icon_url = (        # aller chercher l'icone de openweathermap en temps reel. il s'update a l'ecran dans le pygame
            f"https://openweathermap.org/img/wn/"
            f"{icon_code}@2x.png"
        )

        icon_response = requests.get(icon_url)

        image_file = io.BytesIO(icon_response.content)    # utiliser la bibliotheque io pour traiter l'image de l'icone

        image = pygame.image.load(image_file).convert_alpha()    # convert_alpha garde la transparence de l'image. pour l'afficher sur un fond colore

        api_connecte = True # Une fois connecté, envoi le log qu'il est connecté
        api_connecte_precedent = False
        if api_connecte != api_connecte_precedent:
            connecte = "connecte"
            logapi(connecte)
            api_connecte_precedent = api_connecte

        return {        # retourne les elements pour les afficher dans le pygame
            "temperature": temperature,
            "description": description,
            "image": image,        # image de l'icone
            "city": city,
            "lang": lang,
        }
    
       

    except requests.RequestException as e:      #log les erreurs API -- peut etre déclencher en retirant une lettre du url
        message = str(e)
        message = message.replace(API_KEY,"??????")         #Sinon notre cle API apparait dans le message d'erreur   
        logapi(message)
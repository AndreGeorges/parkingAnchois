import io
import os
import requests
import pygame
from models.logger_manager import logapi
from config.config_loader import OPENWEATHER


# cette fonction appelle openweathermap . elle est importee dans ui_pygame
def get_weather():
    try:  #pour vérifier et logger les Erreurs
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={OPENWEATHER['city']}"        # definie dans config.yaml
            f"&appid={OPENWEATHER['API_KEY']}"        # la cle se trouve dans config.yaml comme le veut la pratique de cacher les infos sensibles
            f"&units=metric"
            f"&lang={OPENWEATHER['lang']}"  # definie dans config.yaml
        )

        response = requests.get(url,timeout=5) # timeout donne 5 secondes max pour se connecter
        response.raise_for_status() #s'assure que l'API est  connecté sinon erreur


        data = response.json()        
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]
        try:
            icon_url = (        # aller chercher l'icone de openweathermap en temps reel. il s'update a l'ecran dans le pygame
                f"https://openweathermap.org/img/wn/"
                f"{icon_code}@2x.png"
            )

            icon_response = requests.get(icon_url)

            image_file = io.BytesIO(icon_response.content)    # utiliser la bibliotheque io pour traiter l'image de l'icone

            verif_icon = os.listdir("assets/weather_icons")     # Verification si l"image existe deja dans le dossier
            if f"{icon_code}.png" not in verif_icon:            # Si non, enregistre l'image
                with open(f"assets/weather_icons/{icon_code}.png","wb") as icon_local:
                    icon_local.write(icon_response.content)

            image_local =pygame.image.load(f"assets/weather_icons/{icon_code}.png").convert_alpha()   # image_local utilisé au lieu de image precedement utilisé
            image = pygame.image.load(image_file).convert_alpha()    # convert_alpha garde la transparence de l'image. pour l'afficher sur un fond colore
        except:
            message = f"L'icone WeatherMap n'a pas chargé"
            logapi(message)
            image_local= pygame.image.load(f"assets/weather_icons/Defaut_Probleme.png")

        api_connecte = True # Une fois connecté, envoi le log qu'il est connecté
        api_connecte_precedent = False
        if api_connecte != api_connecte_precedent:
            connecte = "connecte"
            logapi(connecte)
            api_connecte_precedent = api_connecte

        return {        # retourne les elements pour les afficher dans le pygame
            "temperature": temperature,
            "description": description,
            "image": image_local,        # image de l'icone
            "city": OPENWEATHER['city'],
            "lang": OPENWEATHER['lang'],
        }
    
       

    except requests.RequestException as e:      #log les erreurs API -- peut etre déclencher en retirant une lettre du url
        message = str(e)
        message = message.replace(OPENWEATHER['API_KEY'],"??????")         #Sinon notre cle API apparait dans le message d'erreur   
        logapi(message)
import pygame
from datetime import datetime
import requests
from config import API_KEY, SCREEN_COLOR, TARIFS, BOUTONS_PHYSIQUES
from api import get_weather
from liste_vehicules import *
from utils import get_screen_color, draw_keyboard, get_color, get_tarif,draw_button,liste_bouton,bouton_accueil,eviter_surcharge_etat

pygame.init()
import io  # pour que l'image de weathermap.org s'affiche
from time import asctime
from shared_state import update_data, get_data
import threading
from main import parking_system  # voila un element important dans la jonction des 2 fichiers main et pygame: le while true de main est dans une fonction qui est importee ici

W = 1000
H = 800
marge_gauche = 40

screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Stationnement OZ'Anchois")# nom au dessus de la fenetre
image_fond = pygame.image.load("fond.jpg") # image de fond avec ecrans statique
image_fond = pygame.transform.scale(image_fond,(W,H))

weather = get_weather()   # recupere la weather qui est dans API. et le met dans variable. on pourra l'appeler plus tard, ex: weather["city"]

clock = pygame.time.Clock()

etat_pg = "IDLE"
place_pg = 5
input_text = ""    # recueille le texte entre au clavier numerique par l'utilisateur

# !!! lance parking_system()  du main dans un THREAD
# ca evite d'avoir 2 while true en meme temps ( celui du main et celui du pygame )
thread_main = threading.Thread(target=parking_system, daemon=True)  # daemon veut dire en arriere plan. il est evidemment a True
thread_main.start()

active = False

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            update_data(running = "False")            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            for rect, letter in key_rect:               # recueille le texte entre au clavier numerique par l'utilisateur
                if rect.collidepoint(event.pos):
                    input_text += letter
            if delete_button.collidepoint(event.pos):                  # DELETE BUTTON rendu actif
                input_text = input_text[:-1]                # efface le caractere precedent
            if enter_button.collidepoint(event.pos):                # ENTER BUTTON update_data va mettre input_text dans user_input du shared_state
                update_data(
                    user_input = input_text,
                    input_ready = True
                )
                input_text = ""

                #  Le bouton accueil ne fonctionne presentement pas
            # if retour_accueil.collidepoint(event.pos):                # bouton retour a l'accueil a implementer
            #     etat_precedent = shared["etat"]
            #     print(etat_precedent,"ava")
            #     update_data(etat = "IDLE")
            #     shared=get_data()
            #     etat = shared["etat"]
            #     print(etat,"apre")

            for bouton,duree in liste_bouton:               # Boutons pour la selection de duree 
                if bouton.collidepoint(event.pos):              #ils retournent la duree de la liste TARIF donc peuvent etre changé sans faire plein d modifications
                    update_data(
                    user_input = duree,
                    input_ready = True
                    )   
                    input_text = ""  # vide la zone de texte

                    
    shared = get_data()  # recevoir les inputs du shared_state
    
    # placer les etats qu'on a recu du shared_state dans des variables pour s'en servir ici
    # ils ont ete passes du main via update_data ( v. dans le while true du main)
    etat_pg = shared["etat"]
    event_pg = shared["event"]
    place_pg = shared["places"]
    tarif_pg = shared["tarif"]
    vehicule_pg = shared["vehicule_id"]
    file_attente_pg = shared["file_attente"]    # c'est en fait la liste de vehicule. elle a ete passee dans le main:  file_attente=list(liste_vehicules),
    historique_pg = shared["historique"]
    transactions = shared["transactions"]
    message_pg = shared["message"]
    keyboard = shared["keyboard"]
    
# placer la variable recuperee dans une variable qu'on va utiliser ici
    file_attente_pg = list(file_attente_pg)
    
    horloge = datetime.now().strftime("%H:%M:%S")
    screen.blit(image_fond,(0,0))
    overlay = pygame.Surface((1000,800),pygame.SRCALPHA)  #  pour faire le rectangle transparent
    couleur = get_screen_color(etat_pg, SCREEN_COLOR)
    pygame.draw.rect(overlay,(*couleur,50),(0,0,1000,800))
    screen.blit(overlay,(0,0))

    # screen.fill(get_screen_color(etat_pg, SCREEN_COLOR))      # SCREEN_COLOR se trouve dans config.py


    font = pygame.font.SysFont(None, 24)

    # on utilise la variable etat_pg issue de     etat_pg = shared["etat"] (v. plus haut)
    text = font.render(f"Etat Actuel: {etat_pg}", True, get_color("JAUNE"))      #BLUE toutes les couleurs sont dans config.py. la fonction get_color est dans config.py
    screen.blit(text, (marge_gauche, 40))

    # on utilise la variable place_pg issue de     place_pg = shared["places"] (v. plus haut)
    text = font.render(f"Nb de places restantes: {place_pg} / 5", True, get_color("BLUE"))
    screen.blit(text, (marge_gauche, 80))

    # affiche TARIFS
    y_offset = 40
    text_headers = "{:<20} {:<20} {:<20}".format("TARIF", "DUREE", "PRIX")
    headers = font.render(text_headers, True, get_color("JAUNE"))
    screen.blit(headers, (300, y_offset))  
    y_offset +=25
    for duree, prix in TARIFS.items():        # on a importe plus haut les TARIFS de config.py
        text_duree=f"{str(duree)+ ' h'}"
        text_prix=f"{prix} $"
        screen.blit(font.render(text_duree,True, get_color("BLUE")) ,(430, y_offset))
        screen.blit(font.render(text_prix,True, get_color("BLUE")), (540, y_offset))
        y_offset += 20
        
    # AFFICHAGE WEATHER
    # pygame.draw.rect(screen, get_color("GRIS"), (675, 10, 250, 170), border_radius=21) 
    image_big = pygame.transform.scale(weather["image"], (220, 220))

    overlay = pygame.Surface((200,88),pygame.SRCALPHA)  #  pour faire le rectangle transparent
    pygame.draw.rect(overlay,(255,255,255,128),(0,0,300,120),border_radius=21)
    screen.blit(image_big, (760, 0))
    # screen.blit(overlay,(690,15))

    # AFFICHAGE HORLOGE
    text = font.render(f"Horloge: {horloge}", True, get_color("BLUE"))
    screen.blit(text, (685, 50))

    text = font.render(f"{weather["city"]}: {weather["temperature"]} °C", True, get_color("BLUE"))
    screen.blit(text, (685, 80))

    text = font.render(f"{weather["description"]}", True, get_color("BLUE"))
    screen.blit(text, (685, 110))

    # AFFICHE VEHICULE CURRENT
    text = font.render(f"Vehicule: {vehicule_pg}", True, get_color("JAUNE"))
    screen.blit(text, (marge_gauche, 164))

    # FILE ATTENTE
    # pygame.draw.rect(screen, get_color("GRIS"), (10, 190, W-20, 130), border_radius=21) 
    text = font.render(f"File d'attente: ", True, get_color("JAUNE"))
    screen.blit(text, (marge_gauche, 200))
    
    y_offset = 200
    text_headers = "{:<40} {:<40} {:<40}".format("vehicule_id", "heure_arrivee", "heure_depart")    # faire des headers en haut des colonnes
    headers = font.render(text_headers, True, get_color("JAUNE"))
    screen.blit(headers, (250, y_offset))  
    y_offset +=25

    for veh in file_attente_pg:                                                                     # rendre la liste de vehicules de file_attente_pg (qui est liste_vehicule dans le main)
        heure_ar_lisible = datetime.fromtimestamp(veh["heure_arrivee"]).strftime("%H:%M:%S")        # convertir le temps epoch en temps lisible 
        heure_dep_lisible = datetime.fromtimestamp(veh["heure_depart"]).strftime("%H:%M:%S")
        text_id=f"{veh['vehicule_id']}"
        text_heure_ar=f"{heure_ar_lisible}"
        text_heure_dep=f"{heure_dep_lisible}" 
        screen.blit(font.render(text_id,True, get_color("BLUE")) ,(250, y_offset))
        screen.blit(font.render(text_heure_ar,True, get_color("BLUE")), (475, y_offset))
        screen.blit(font.render(text_heure_dep,True, get_color("BLUE")), (685, y_offset))
        y_offset += 20

    # HISTORIQUE TRANSACTIONS
    # pygame.draw.rect(screen, get_color("GRIS"), (10, 340, W-20, 150), border_radius=21) 
    text = font.render(f"Historique Transactions: ", True, get_color("JAUNE"))
    screen.blit(text, (marge_gauche, 350))
    
    y_offset = 350
    text_headers = "{:<40} {:<40} {:<40}".format("heure", "vehicule ID", "evenement")    # faire des headers en haut des colonnes
    headers = font.render(text_headers, True, get_color("JAUNE"))
    screen.blit(headers, (250, y_offset))  
    y_offset +=25
    for trans in transactions[-5:]:                         # rendre la liste de transactions v. plus haut (transactions = shared["transactions"])
        text_heure=f"{trans['heure']}"
        text_id=f"{trans["vehicule_id"]}"
        text_evenement=f"{trans["evenement"]}" 
        screen.blit(font.render(text_heure,True, get_color("BLUE")) ,(250, y_offset))
        screen.blit(font.render(text_id,True, get_color("BLUE")), (437, y_offset))
        screen.blit(font.render(text_evenement,True, get_color("BLUE")), (620, y_offset))

        y_offset += 20

    # afficher les messages venant du main, comme        update_data(message="Entrez le numero de plaque de votre voiture: ") 
    text = font.render(f"Message: {message_pg}", True, get_color("VERT_POMME"))
    screen.blit(text, (marge_gauche, 518))

    # faire apparaitre le KEYBOARD, passer ce qu'on ecrit dans l'input box
    if shared["keyboard"] == False:
        bouton_duree = draw_button(screen,font)
    else:
        input_box, key_rect, delete_button, enter_button = draw_keyboard(screen, font, input_text)  
    
    # le bouton accueil ne fonctionne presentement pas
    #retour_accueil = bouton_accueil(screen,font) # affiche le bouton retour a l'accueil


    # affiche BOUTONS PHYSIQUES
    y_offset = 580
    for btn, fonction in BOUTONS_PHYSIQUES.items():
        text_str = f"Bouton {str(btn)} : {fonction}"
        text_surface = font.render(text_str, True, get_color("BLUE"))    
        screen.blit(text_surface, (600, y_offset))
        y_offset += 20








    pygame.display.flip()
    clock.tick(30)




pygame.quit()
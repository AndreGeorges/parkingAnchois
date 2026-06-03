import pygame
from config.config_loader import TARIFS, SCREEN_COLOR, COLOR
from config.logsconfig import logchetat, logevent
from comm import sendEmail

# cette fonction evite au logging de se repeter
def eviter_surcharge_etat(etat, etat_precedent):
    if etat != etat_precedent:
        print(f"Etat: {etat.value}")
        sendEmail(etat.value,None)               # email base au changement d'etat
        logchetat(etat, etat_precedent)         #log du changement d'etat
        etat_precedent = etat        # l'etat sera affiche seulement s'il est different de l'etat precedent. 
    return etat, etat_precedent

# cette fonction evite au logging de se repeter
def eviter_surcharge_event(event, event_precedent):
    if event != event_precedent:
        print(f"Event: {event.value}")
        logevent(event.value)               # log base sur changement d'evenement
        sendEmail(None,event.value)     # email base sur le changement d'etat
        event_precedent = event        # l'evenement sera affiche seulement s'il est different de l'evenement precedent. 
    return event, event_precedent

def get_tarif(duree, TARIFS):
    return TARIFS.get(duree)

def get_screen_color(etat_pg, SCREEN_COLOR):
    return SCREEN_COLOR.get(etat_pg)

ROWS = ["0123456789", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
KEY_SIZE = 40
SPACE_BTW = 5


# CECI DESSINE LE KEYBOARD DANS LE PYGAME
def draw_keyboard(screen, font, input_text):
    key_rect = []
    max = 0
    
    for row_index, row in enumerate(ROWS):
        x_offset = 40   # definir position depart horizontal
        y_offset = 565    # definir position depart vertical, apres les autres affichages
        for keyb_index, letter in enumerate(row):
            if keyb_index > max:
                max = keyb_index    # variable 'max' garde la largeur totale du keyboard
            x = x_offset + keyb_index * (KEY_SIZE + SPACE_BTW)
            y = y_offset + row_index * (KEY_SIZE + SPACE_BTW)
            rect = (pygame.Rect( x, y, KEY_SIZE, KEY_SIZE))
            key_rect.append((rect, letter))
            pygame.draw.rect(screen, get_color("BLACK"), rect)
            
            text_surf = font.render(letter, True,  get_color("WHITE"))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            
            y_input = y_offset + (len(ROWS) * (KEY_SIZE + SPACE_BTW))    # positionne curseur en bas des rows precedents ( compte nb de rows + l'offset de y)
            width = (max + 1) * (KEY_SIZE + SPACE_BTW) - SPACE_BTW  # calcule  la largeur totale du keyboard et le met dans variable 'width'
            
    # INPUT BOX
            
    input_box = pygame.Rect(x_offset, y_input, width-136, KEY_SIZE)    # dessiner l'input box ( le fond )
    pygame.draw.rect(screen, get_color("WHITE"), input_box,0,10)
    
    text_surface = font.render(input_text, True, get_color("BLUE"))   # rendre le texte dans l'input box
    text_rect = text_surface.get_rect()
    text_rect.center = input_box.center # Center the input text in the text field box
    screen.blit(text_surface, text_rect)
    
    #  DELETE BUTTON

    delete_button = pygame.Rect( (width - KEY_SIZE), (y_offset + 2* (KEY_SIZE + SPACE_BTW)) , (2*KEY_SIZE), KEY_SIZE )  # definit le bouton delete
    txt_delete = "DELETE"
    pygame.draw.rect(screen, get_color("BLACK"), delete_button )   # dessine le rectangle du bouton
    delete_text = font.render(txt_delete, True, get_color("WHITE"))   # definit le texte du bouton
    delete_text_rect = delete_text.get_rect(center=delete_button.center)   # place le texte dans le bouton
    screen.blit(delete_text, delete_text_rect)    # affiche (le texte, le conteneur)
    
    #  ENTER BUTTON
    
    enter_button = pygame.Rect( (width - 2* KEY_SIZE - 2*SPACE_BTW ), (y_offset + 3* (KEY_SIZE + SPACE_BTW)) , (3* (KEY_SIZE + SPACE_BTW)-5), KEY_SIZE )  # definit le bouton ENTER   
    txt_enter = "ENTER"
    pygame.draw.rect(screen, get_color("BLACK"), enter_button )   # dessine le rectangle du bouton
    enter_text = font.render(txt_enter, True, get_color("WHITE"))   # definit le texte du bouton
    enter_text_rect = enter_text.get_rect(center=enter_button.center)   # place le texte dans le bouton
    screen.blit(enter_text, enter_text_rect)    # affiche (le texte, le conteneur)
    
    
    return input_box, key_rect, delete_button, enter_button
liste_bouton = []
def draw_button(screen, font):
    
    y_offset = 570
    for duree, prix in TARIFS.items():        # on a importe plus haut les TARIFS de config.py
        boutons_duree = pygame.Rect(200,y_offset,120,30)
        liste_bouton.append((boutons_duree,duree))
        text_duree=f"{str(duree)}h pour {prix} $"
        pygame.draw.rect(screen,get_color("JAUNE"),(200,y_offset,120,30),border_radius=10)
        text_duree_prix=font.render(text_duree,True, get_color("BLUE"))
        text_duree_prix_rect = text_duree_prix.get_rect(center=boutons_duree.center)
        screen.blit(text_duree_prix,text_duree_prix_rect)
        
        y_offset += 45

def bouton_accueil(screen,font):
    boutons_accueil = pygame.Rect(365,744,120,40)
    accueil="ACCUEIL"
    pygame.draw.rect(screen,get_color("VIOLET"),boutons_accueil,border_radius=10)
    text_accueil=font.render(accueil,True, get_color("WHITE"))
    text_accueil_rect = text_accueil.get_rect(center=boutons_accueil.center)
    screen.blit(text_accueil,text_accueil_rect)
    return boutons_accueil



# cette fonction permet de retourner la couleur
def get_color(color_name):
    return COLOR[color_name]

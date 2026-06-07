from tkinter import *
from config.ui_config import get_color_rgb, get_AUTH
from models.parking import update_data, get_data     # echanger les donnes avec pygame via shared_state


# relx et rely vont placer selon les pourcentages de la fenêtre, anchor va permettre de placer le widget selon un point d'ancrage (ici le centre) 
# padx et pady vont ajouter des marges entre les widgets

AUTH=get_AUTH() #Récupère les informations de configuration pour la vue d'authentification à partir du fichier de configuration et les stocke dans la variable AUTH.
texte_info =AUTH["info_texte"] #Récupère les informations de configuration pour le texte de la vue d'authentification à partir du fichier de configuration et les stocke dans la variable texte_info.


#==================================== Variables de configuration de la fenêtre ====================================

# fenêtre principale
largeur_fenetre = AUTH["largeur_fenetre"]
hauteur_fenetre = AUTH["hauteur_fenetre"]
nom_fenetre = AUTH["nom_fenetre"]
couleur_fond = get_color_rgb(AUTH["couleur_fond"])

# barre de titre
couleur_barre_titre = get_color_rgb(AUTH["couleur_barre_titre"])
couleur_titre = get_color_rgb(AUTH["couleur_titre"])
font_titre = (texte_info["font_titre"], texte_info["taille_titre"], texte_info["style_titre"])

# texte
couleur_texte = get_color_rgb(AUTH["couleur_texte"])
texte = AUTH["texte"]
font_texte = (texte_info["font_texte"], texte_info["taille_texte"])

# clavier numérique
boutons_numeriques = AUTH["boutons_numeriques"]
couleur_ecran= get_color_rgb(AUTH["couleur_ecran"])
font_ecran = (texte_info["font_ecran"], texte_info["taille_ecran"])




#================================ Fonctions de l'interface utilisateur ====================================

def charger_interface():
    global code_reel, texte_ecran, boutons_fonctionnels
    fenetre = Tk()
    code_reel = ""
    texte_ecran = StringVar() #Variable pour stocker le texte affiché à l'écran, utilisée pour capturer les événements de clavier


    # Pour centrer la fenêtre sur l'écran 
    def centrer_fenetre(ecran, largeur, hauteur):    
        largeur_ecran = ecran.winfo_screenwidth()      #Récupère la largeur de l'écran
        hauteur_ecran = ecran.winfo_screenheight()     #Récupère la hauteur de l'écran
        x = (largeur_ecran - largeur) // 2
        y = (hauteur_ecran - hauteur) // 2
        ecran.geometry(f"{largeur}x{hauteur}+{x}+{y}")


    # Fonction pour créer l'écran de saisie du code
    def ecran(fenetre):
        global texte_ecran, ecran, code_reel
        frame_ecran =Frame(fenetre, bg=couleur_ecran, height=50,width=200,borderwidth=5, relief="groove")  #Crée une frame pour l'écran
        frame_ecran.place(relx=0.5, rely=0.2, anchor="center")   #Place la frame en haut de la fenêtre mais décalé un peu vers le bas pour laisser un espace entre l'écran et le bord de la fenêtre
        texte_ecran.set("") #Initialise le texte de l'écran à une chaîne vide
        code_reel =("") #Variable pour stocker le code réel entré par l'utilisateur
        ecran = Label(fenetre, textvariable=texte_ecran, bg=couleur_ecran, font=font_ecran) #Crée un label pour capturer les événements de clavier
        ecran.place(relx=0.5, rely=0.2, anchor="center") #Place le label de l'écran au centre de la fenêtre et lui permet de s'étendre pour remplir l'espace disponible
    
    # Fonction pour créer le clavier numérique
    def draw_keyboard(fenetre):
        frame_clavier = Frame(fenetre, bg=couleur_fond) #Crée une frame pour le clavier
        frame_clavier.place(relx=0.5, rely=0.55, anchor="center") #Place la frame du clavier au centre de la fenêtre              
        for i, row in enumerate(boutons_numeriques):
            for j, key in enumerate(row):
                if key == "":
                    continue
                Button(frame_clavier, text=key, width=5, height=2, font=font_texte,command=lambda k=key: entree_clavier(k)).grid(row=i, column=j, padx=10, pady=10) #Crée un bouton pour chaque chiffre et le place dans la frame du clavier

    # Fonction pour gérer l'entrée du clavier numérique
    def entree_clavier(key):
        global code_reel
        code_reel += key
        texte_ecran.set("*" * len(code_reel))  # Affiche des étoiles pour chaque caractère entré

    # Fonctions des boutons fonctionnels
    def effacer():
        global code_reel
        code_reel = code_reel[:-1]  # Supprime le dernier caractère du code réel
        texte_ecran.set("*" * len(code_reel))  # Met à jour l'affichage avec des étoiles

    def valider():
        global code_reel
        update_data(code_saisi=code_reel)
        fenetre.destroy()
        

    def annuler():
        update_data(code_saisi="")
        fenetre.destroy()

    # Dictionnaire pour stocker les propriétés des boutons fonctionnels nom du bouton, couleur de fond et la commande associée
    boutons_fonctionnels = { "Valider":{"bg":"green","commande":valider},"Effacer":{"bg":"orange","commande":effacer}, "Annuler":{"bg":"red","commande":annuler}}

    # Fonction pour créer les boutons fonctionnels
    def draw_boutons(fenetre):
        global effacer, valider,boutons_fonctionnels
        frame_boutons = Frame(fenetre,bg=couleur_fond) #Crée une frame pour les boutons
        frame_boutons.place(relx=0.5,rely=0.9,anchor="center") #Place les boutons en bas de la fenêtre
        for i, (key, properties) in enumerate(boutons_fonctionnels.items()):
            Button(frame_boutons, text=key, width=10, height=2, font=font_texte, bg=properties["bg"], command=properties["commande"]).grid(row=0, column=i, padx=10)
        
        # Création de la Barre de titre
    def draw_barre_titre(fenetre):
        #fenetre.overrideredirect(True)          # Retire les bordures et la barre de titre de la fenêtre
        frame_titre =Frame(fenetre, bg=couleur_barre_titre, height=38,borderwidth=5, relief="groove")  #Crée une frame pour la barre de titre personnalisée
        frame_titre.pack(fill="x", side="top",padx=10,pady=10)   #Place la frame en haut de la fenêtre mais décalé un peu vers le bas pour laisser un espace entre la barre de titre et le bord de la fenêtre
        frame_titre.pack_propagate(False)   #Empêche la frame de redimensionner automatiquement pour s'adapter à son contenu
        label_titre = Label(frame_titre, text=f"  {nom_fenetre.upper()}  ", bg=couleur_barre_titre, fg=couleur_titre, font=font_titre)  #Crée un label pour le titre de la barre de titre personnalisée
        label_titre.pack(pady=0)   #Place le label au centre de la frame de la barre de titre personnalisée

    # Texte fixe qui ne change pas, pour le message "Entrez votre code : "
    def texte_fix(fenetre):
        global label_texte
        label_texte = Label(fenetre, text=texte,bg=couleur_fond,  fg=couleur_texte, font=font_texte) #Crée un label pour le texte
        label_texte.place(relx=0.5, rely=0.12, anchor="center")  #Place le label de texte du message

    # Création de la fenêtre principale
    def create_window(fenetre):
        #fenetre = Tk()
        centrer_fenetre(fenetre, largeur_fenetre, hauteur_fenetre)
        fenetre.configure(bg=couleur_fond,borderwidth=5, relief="sunken") #Configure la couleur de fond et les bordures de la fenêtre
        fenetre.title(nom_fenetre) # titre au cas où overridedirect est retiré
        fenetre.resizable(False, False)     #Empêche la redimension de la fenêtre
        fenetre.grab_set() # Empêche l'utilisateur d'interagir avec d'autres fenêtres tant que celle-ci est ouverte
        fenetre.focus_force() # Force la fenêtre à prendre le focus quand la fenêtre est ouverte en tant que fenêtre modale ou si elle est superposée à d'autres fenêtres. 
                                # Cela garantit que l'utilisateur peut interagir avec la fenêtre immédiatement après son ouverture sans avoir à cliquer dessus pour lui donner le focus.
        return fenetre



    #==========================Appel des fonctions pour créer les différentes parties de l'interface utilisateur==========================

    
    create_window(fenetre) #Appelle la fonction pour créer la fenêtre principale
    texte_fix(fenetre) #Appelle la fonction pour créer le texte fixe
    draw_barre_titre(fenetre) #Appelle la fonction pour créer la barre de titre personnalisée
    ecran(fenetre) #Appelle la fonction pour créer l'écran de saisie du code
    draw_keyboard(fenetre) #Appelle la fonction pour créer le clavier numérique
    draw_boutons(fenetre) #Appelle la fonction pour créer les boutons fonctionnels (Effacer, Valider, Annuler)
        
        
        
    
    fenetre.mainloop()



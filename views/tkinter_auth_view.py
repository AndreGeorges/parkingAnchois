from tkinter import *
from tkinter import ttk






# relx et rely vont placer selon les pourcentages de la fenêtre, anchor va permettre de placer le widget selon un point d'ancrage (ici le centre) 
# padx et pady vont ajouter des marges entre les widgets

# Variables de configuration de la fenêtre

largeur_fenetre = 500
hauteur_fenetre = 700
nom_fenetre = "Parking OZ Anchois"
couleur_fond = "lightblue"
couleur_barre_titre = "blue"
couleur_titre = "white"
font_titre = ("Arial bold", 18,"bold italic underline")
couleur_texte = "black"
texte = "Entrez votre code : "
font_texte = ("Arial", 14)
boutons_numeriques = [["1","2","3"], ["4","5","6"], ["7","8","9"], ["","0",""]]

code_reel =("") #Variable pour stocker le code réel entré par l'utilisateur
couleur_ecran= "white"
font_ecran = ("Arial", 16)


# Pour centrer la fenêtre sur l'écran 
def centrer_fenetre(ecran, largeur, hauteur):
    
    largeur_ecran = ecran.winfo_screenwidth()      #Récupère la largeur de l'écran
    hauteur_ecran = ecran.winfo_screenheight()     #Récupère la hauteur de l'écran
    x = (largeur_ecran - largeur) // 2
    y = (hauteur_ecran - hauteur) // 2
    ecran.geometry(f"{largeur}x{hauteur}+{x}+{y}")

def ecran():
    global texte_ecran, ecran
    frame_ecran =Frame(fenetre, bg=couleur_ecran, height=50,width=200,borderwidth=5, relief="groove")  #Crée une frame pour l'écran
    frame_ecran.place(relx=0.5, rely=0.2, anchor="center")   #Place la frame en haut de la fenêtre mais décalé un peu vers le bas pour laisser un espace entre l'écran et le bord de la fenêtre
    texte_ecran = StringVar() #Variable pour stocker le texte affiché à l'écran, utilisée pour capturer les événements de clavier
    texte_ecran.set("") #Initialise le texte de l'écran à une chaîne vide
    ecran = Label(fenetre, textvariable=texte_ecran, bg=couleur_ecran, font=font_ecran) #Crée un label pour capturer les événements de clavier
    ecran.place(relx=0.5, rely=0.2, anchor="center") #Place le label de l'écran au centre de la fenêtre et lui permet de s'étendre pour remplir l'espace disponible
  

def draw_keyboard():
    frame_clavier = Frame(fenetre, bg=couleur_fond) #Crée une frame pour le clavier
    frame_clavier.place(relx=0.5, rely=0.5, anchor="center") #Place la frame du clavier au centre de la fenêtre              
    for i, row in enumerate(boutons_numeriques):
        for j, key in enumerate(row):
            if key == "":
                continue
            Button(frame_clavier, text=key, width=5, height=2, font=font_texte,command=lambda k=key: entree_clavier(k)).grid(row=i, column=j, padx=10, pady=10) #Crée un bouton pour chaque chiffre et le place dans la frame du clavier


def entree_clavier(key):
    global code_reel
    code_reel += key
    texte_ecran.set("*" * len(code_reel))  # Affiche des étoiles pour chaque caractère entré

def effacer():
    global code_reel
    code_reel = code_reel[:-1]  # Supprime le dernier caractère du code réel
    texte_ecran.set("*" * len(code_reel))  # Met à jour l'affichage avec des étoiles

def valider():
    global code_reel
    if code_reel == "1234":  # Remplacez "1234" par le code réel que vous souhaitez utiliser
        texte_ecran.set("Code correct !")
    else:
        texte_ecran.set("Code incorrect !")
    code_reel = ""

def annuler():
    global code_reel
    code_reel = ""
    texte_ecran.set("")  # Efface l'affichage de l'écran

boutons_fonctionnels = {"Effacer":{"bg":"red","commande":effacer}, "Valider":{"bg":"green","commande":valider}, "Annuler":{"bg":"orange","commande":annuler}}

def draw_boutons():
    global effacer, valider,boutons_fonctionnels
    frame_boutons = Frame(fenetre,bg=couleur_fond) #Crée une frame pour les boutons
    frame_boutons.place(relx=0.5,rely=0.85,anchor="center") #Place les boutons en bas de la fenêtre
    for i, (key, properties) in enumerate(boutons_fonctionnels.items()):
        Button(frame_boutons, text=key, width=10, height=2, font=font_texte, bg=properties["bg"], command=properties["commande"]).grid(row=0, column=i, padx=10)
    



# Création de la fenêtre principale
fenetre = Tk()
centrer_fenetre(fenetre, largeur_fenetre, hauteur_fenetre)
fenetre.configure(bg=couleur_fond,borderwidth=5, relief="sunken") #Configure la couleur de fond et les bordures de la fenêtre
fenetre.title(nom_fenetre) # titre au cas où overridedirect est retiré
fenetre.resizable(False, False)     #Empêche la redimension de la fenêtre

# Barre titre
fenetre.overrideredirect(True)          # Retire les bordures et la barre de titre de la fenêtre
frame_titre =Frame(fenetre, bg=couleur_barre_titre, height=38,borderwidth=5, relief="groove")  #Crée une frame pour la barre de titre personnalisée
frame_titre.pack(fill="x", side="top", pady=10)   #Place la frame en haut de la fenêtre mais décalé un peu vers le bas pour laisser un espace entre la barre de titre et le bord de la fenêtre
frame_titre.pack_propagate(False)   #Empêche la frame de redimensionner automatiquement pour s'adapter à son contenu
label_titre = Label(frame_titre, text=f"  {nom_fenetre.upper()}  ", bg=couleur_barre_titre, fg=couleur_titre, font=font_titre)  #Crée un label pour le titre de la barre de titre personnalisée
label_titre.pack(pady=0)   #Place le label au centre de la frame de la barre de titre personnalisée

# Texte
label_texte = Label(fenetre, text=texte,bg=couleur_fond,  fg=couleur_texte, font=font_texte) #Crée un label pour le texte
label_texte.place(relx=0.25, rely=0.12, anchor="center")  #Place le label de texte du message

# Ecran
ecran() #Appelle la fonction pour créer l'écran de saisie du code
#frame_ecran =Frame(fenetre, bg=couleur_ecran, height=50,width=200,borderwidth=5, relief="groove")  #Crée une frame pour l'écran
#frame_ecran.place(relx=0.5, rely=0.2, anchor="center")   #Place la frame en haut de la fenêtre mais décalé un peu vers le bas pour laisser un espace entre l'écran et le bord de la fenêtre
#texte_ecran = StringVar() #Variable pour stocker le texte affiché à l'écran, utilisée pour capturer les événements de clavier
#texte_ecran.set("") #Initialise le texte de l'écran à une chaîne vide
#ecran = Label(fenetre, textvariable=texte_ecran, bg=couleur_ecran, font=font_ecran) #Crée un label pour capturer les événements de clavier
#ecran.place(relx=0.5, rely=0.2, anchor="center") #Place le label de l'écran au centre de la fenêtre et lui permet de s'étendre pour remplir l'espace disponible

# Boutons
draw_keyboard()
draw_boutons()




fenetre.grab_set()
fenetre.focus_force()
fenetre.mainloop()



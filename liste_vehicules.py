import json
import os
import threading
from time import time, sleep, perf_counter
from config.logsconfig import logerreur


# communique avec le json pour charger les vehicules
def charger():
    try:
        with open('db.json', 'r') as f:
            return json.load(f) 
    except FileNotFoundError as e:
        logerreur(e)
        return []
    
liste_vehicules = charger()

# sauvegarder les vehicules apres 
def sauvegarder(liste_vehicules):
    with open('db.json', 'w') as f:
        json.dump(liste_vehicules, f, indent=4)

# trouver index du vehicule. a voir si on peut faire sans
def trouver_index(vehicule_id):
    for i, rep in enumerate(liste_vehicules):
        if rep["vehicule_id"].lower() == vehicule_id.lower():
            return i
    return -1




# affichage dans la console seulement. pas dans le pygame
def afficher_vehicules(liste_vehicules):

    print(
        "\n============================================== Liste Vehicules ====================================================\n")
    
    if liste_vehicules == []:
        print("# {:<40} {:<40} {:<40}".format("vehicule_id", "heure_arrivee", "heure_depart"))
        print("\nLe stationnement est vide.\n")
    else:
        print("# {:<41} {:<41} {:<41}".format(*liste_vehicules[0].keys()))
        for vehicule in liste_vehicules:
            print(f"\n{liste_vehicules.index(vehicule) + 1}. ""{: <40} {: <40} {: <40}".format(*vehicule.values()))
afficher_vehicules(liste_vehicules)

# la fonction pour charger le fichier transaction.json 
# l'autre partie de gestion de fichier se trouve dans crud.py def sauvegarder_transactions. a voir si on peut le deplacer ici?
def charger_transactions():
    try:
        with open('transactions.json', 'r') as t:
            return json.load(t) 
    except FileNotFoundError as e:
        logerreur(e) 
        return []
    
transactions = charger_transactions()



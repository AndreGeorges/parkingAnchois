from models.vehicle import liste_vehicules, trouver_index,  sauvegarder, transactions
from time import time
from datetime import datetime
import json

# ajoute le vehicule dans liste vehicule. est appele dans le main
def ajouter_vehicule(vehicule_id, heure_arrivee, heure_depart, duree):
    if trouver_index(vehicule_id) != -1:
        return False
    liste_vehicules.append({"vehicule_id": vehicule_id, "heure_arrivee": heure_arrivee, "heure_depart": heure_depart, "duree":duree})
    sauvegarder(liste_vehicules)
    return True

# verifie le ticket ( = si le temps du vehicule est expire ou pas) ! cette fonction n'est plus appelee, maintenant on appuie sur le bouton pour faire sortir les vehicules FIFO
def verification_ticket(vehicule_id):
    for vehicule in liste_vehicules:
        if vehicule["vehicule_id"] == vehicule_id:
            current_time = round(time() % 10000, 2) 
            if current_time > vehicule["heure_depart"]:
                return True
            else: return False
    return False

# identifier le vehicule avec le plus petit temps restant, pour le faire sortir en premier. ca aurait du s'appeler "identifier_vehicule"
# appele dans le main
def sortir_vehicule(liste_vehicules):
    plus_petit_temps_restant = 10000     # cree variable pous stocker le plus petit temps restant. initialiser a valeur tres haute comme le veut la pratique
    vehicule_sortir_premier = ""      # initialise le vehicule a sortir en premier
    for veh in liste_vehicules:         # parcourir liste vehicules. si on trouve temps plus petit que plus_peti_temps_restant, ecraser la variable avec nouvelle valeur
        temps_restant = int(veh['heure_depart'])  - int(time())
        if temps_restant < plus_petit_temps_restant:
            plus_petit_temps_restant = temps_restant
            vehicule_sortir_premier = veh['vehicule_id']
    return vehicule_sortir_premier      # retourne le vehicule a sortir en premier

# recupere le vehicule a sortir en premier retourne par sortir_vehicule et le supprime
# appele dans le main
def supprimer_vehicule(vehicule_sortir_premier):
    for veh in liste_vehicules:
        if veh['vehicule_id'] == vehicule_sortir_premier:
            liste_vehicules.remove(veh)
    sauvegarder(liste_vehicules)
    return True
  
  
# FONCTION POUR LOGGER LES TRANSACTIONS
# appele dans le main, ou il recolte vehicule_id, element. il recolte aussi transaction, qui est dans update_data
def sauvegarder_transactions(vehicule_id, event, transactions):
    transaction = {
        "heure": datetime.now().strftime("%H:%M:%S"),
        "vehicule_id" : vehicule_id,
        "evenement": event.value
    }
    transactions.append(transaction)    # sauvegarde le fichier transaction
    with open('data/transactions.json', 'w') as t:        # utilise un fichier jason pour sauvegarder les transactions
        json.dump(transactions, t, indent=4)        # acceder au trnsaction.json ici
        
    print("transaction ajoutee:  ", transaction)
    return transactions

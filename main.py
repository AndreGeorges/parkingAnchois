
from time import sleep, time
from datetime import datetime
from etats import Etats, Event
from gpio_manager import *
from config.config import sender_email, recipient_email, app_password, TARIFS 
from utils import eviter_surcharge_etat, eviter_surcharge_event, get_tarif
from liste_vehicules import liste_vehicules, afficher_vehicules, transactions
from crud import ajouter_vehicule, supprimer_vehicule, verification_ticket, sortir_vehicule, sauvegarder_transactions
import threading
from shared_state import update_data, get_data     # echanger les donnes avec pygame via shared_state
import ui_pygame
from config.logsconfig import logerreur
from comm import sendEmail

# initialisation necessaire de certaines variables
etat = Etats.IDLE
etat_precedent = None
event = Event.DEFAULT
event_precedent = Event.DEFAULT
vehicule_id = None
tarif = 0
rappel_lance = False
notif_expire = False
stop_rappel = threading.Event()
stop_temps_expire = threading.Event()
vehicule_sortir_premier = ""

# pour accepter l'input de l'utilisateur et le transferer a ui_pygame via shared_state
def attendre_input():
    while True:         # assurer la continuite de l'echange
        shared = get_data()        # get_data() se trouve dans shared_state
        if shared["input_ready"]:                # if TRUE :  un nouvel input a ete ajoute 
            valeur = shared["user_input"]                # on place l'input dans 'valeur'
                                            # update_data se trouve dans shared_state
            update_data(                   # nettoyer le input une fois qu'on a fini de s'en servir
                input_ready = False,
                user_input = ""
            )
            
            return valeur

# thread envoyer rappel
def envoyer_rappel():
    while not stop_rappel.is_set():
        current_time = int(time())  
        for veh in liste_vehicules:
            if (current_time >= veh["heure_depart"] - 2.5 and current_time <= veh["heure_depart"]):
                update_data(message=f"Le temps du vehicule immatricule  {veh["vehicule_id"]}  va expirer sous peu. ")
                update_data(vehicule_id = veh["vehicule_id"])
                sendEmail(etat.value,None)
                stop_rappel.set()
                break
    sleep(0.2)

# thread temps expire
def temps_expire():
    while not stop_temps_expire.is_set():
        current_time = int(time())  
        for i, rep in enumerate(liste_vehicules):
            if (current_time > rep["heure_depart"]):
                print("Le temps du vehicule immatricule: ", rep["vehicule_id"],  " est expire")
                stop_temps_expire.set()  
                break   
    sleep(0.2)   

 



        
def getEvent(etat, etat_precedent):
    if capt_veh_entre.is_pressed:
        sleep(0.2)
        return Event.VEHICULE_DETECTE
    if select_duree.is_pressed:
        sleep(0.2)
        global vehicule_id, duree, tarif
        # ces fonctions sont dans shared_state et vont renvoyer l'input pour l'afficher dans pygame
        update_data(message="Entrez le numero de plaque de votre voiture: ")          # afficher ce message dans pygame
        vehicule_id = attendre_input()           # capter l'input de l'utlisateur et le mettre dans vehicule_id qui sera passee dans update_data
        update_data(message="Veuillez selectionner la duree de stationnement:  ",
                    keyboard=False)
        duree = int(attendre_input()*10)
        temps_affiche = int(duree/10)
        tarif = get_tarif(temps_affiche, TARIFS)         # get_tarif se trouve dans utils
        update_data(message=f"Duree choisie:  {temps_affiche}  heure(s). Tarif: $ {tarif} Bouton 3: confirmer le paiement  Bouton 5: Annuler la transaction") 
        return Event.DUREE
    if confirm_paiement.is_pressed:
        sleep(0.2)
        return Event.DUREE_PAIEMENT_EFFECTUE
    if capt_veh_sort.is_pressed:
        sleep(0.2)
        return Event.DEMANDE_SORTIE
    if annul.is_pressed:
        sleep(0.2)
        rouge()
        buzzer_court()
        return Event.ANNULATION
    if erreur.is_pressed:
        sleep(0.2)
        rouge()
        buzzer_court()
        return Event.ERREUR
    if err_idle.is_pressed:
        sleep(0.2)
        return Event.RETOUR_IDLE  
    if idle_ferme.is_pressed:
        sleep(0.5)
        if etat == Etats.IDLE:
            return Event.FERME
        else:
            return Event.RETOUR_IDLE       
    # else:
    #     return Event.DEFAULT  # J'ai retiré ceci pour ne pas qu'il loop constamment
    

# mettre boucle while dans une fonction qui est importee dans ui_pygame
def parking_system():
    global etat, event, event_precedent, etat_precedent      # variables precedentes deviennent globales et  sont passees dans update_data ci-dessous
    global vehicule_id, tarif, rappel_lance, notif_expire

    try:
        while True:
            try:  # pour garder dans la loop en cas d'erreur
                update_data(                  # update_data se trouve dans shared_state et fait passer les variables globales ci-haut
                    etat=etat.value if hasattr(etat, "value") else str(etat),
                    event=event.value if hasattr(event, "value") else str(event),
                    places=5 - len(liste_vehicules),
                    tarif=tarif,
                    vehicule_id=vehicule_id,
                    file_attente=list(liste_vehicules),
                    historique=str(liste_vehicules),
                    transactions=list(transactions),
                    keyboard = True,
                )

                match event:
                    case Event.VEHICULE_DETECTE:
                        event, event_precedent = eviter_surcharge_event(     # cette fonction est dans utils.py et evite d'afficher plusieurs fois l'etat dans le logging
                            event, event_precedent
                        )
                        etat = Etats.ATTENTE_ENTREE

                    case Event.PLACE_DISPONIBLE:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.PAIEMENT_ENTREE

                    case Event.PLACE_INDISPONIBLE:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.IDLE

                    case Event.DUREE_PAIEMENT_EFFECTUE:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.ACCES_ACCEPTE

                    case Event.BARRIERE_ENREGISTREMENT_TICKET:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.STATIONNEMENT

                    case Event.DEMANDE_SORTIE:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.ATTENTE_SORTIE

                    case Event.DETECTE_SORTIE_TICKET:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.IDLE

                    case Event.ANNULATION:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.IDLE

                    case Event.ERREUR:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.ERREUR

                    case Event.RETOUR_IDLE:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.IDLE
                    case Event.FERME:
                        event, event_precedent = eviter_surcharge_event(
                            event, event_precedent
                        )
                        etat = Etats.FERME


                match etat:
                    case Etats.IDLE:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        vert()                    # dans gpiomanager. fait que allume la verte et eteint tout le reste
                        event = getEvent(etat, etat_precedent)
                        sleep(0.5)

                    case Etats.FERME:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        rouge() # dans gpiomanager.
                        event = getEvent(etat, etat_precedent)
                        sleep(0.5)

                    case Etats.ATTENTE_ENTREE:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        if len(liste_vehicules) >= 5:
                            rouge()
                            update_data(message="Le parking est plein; veuillez revenir plus tard")
                            sleep(5)
                            event = Event.PLACE_INDISPONIBLE
                            sendEmail(None,event.value)
                            
                        else:
                            jaune()
                            update_data(message=f"Il y a {5 - len(liste_vehicules)} place(s) disponible(s).")
                            event = Event.PLACE_DISPONIBLE
                            sleep(0.5)

                    case Etats.PAIEMENT_ENTREE:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        jaune_blink()  # dans gpiomanager.
                        event = getEvent(etat, etat_precedent)
                        sleep(0.5)

                    case Etats.ACCES_ACCEPTE:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        # remplir variables avec le temps en secondes pour faciliter le calcul
                        heure_arrivee = int(time())                    # time est caste en int pour enlever les digits apres la virgule, qui sont des milisecondes
                        heure_depart = int(time()) + (int(duree) * 10)     # calculer l'heure de depart en ajoutant la DUREE a l'heure de maintenant
                        ajouter_vehicule(vehicule_id, heure_arrivee, heure_depart, duree)      # def dans crud.py ajouter le nouveau vehicule a la liste de vehicules
                        
                        buzzer_court() # dans gpiomanager.
                        barriere_ouvert() # dans gpiomanager.
                        vert()
                        # ci-dessous, preparer variables avant de les mettre dans sauvegarder_transaction. 
                        heure_dep_lisible = datetime.fromtimestamp(heure_depart).strftime("%H:%M:%S")   # pas de calcul necessaire pour transactions, on doit slmt l'afficher. le convertir tout de suite en heure lisible
                        update_data(message=f"Vehicule ajoute.Vous pouvez rester jusqu'a {heure_dep_lisible}")
                        barriere_ferme()
                        event = Event.BARRIERE_ENREGISTREMENT_TICKET
                        sauvegarder_transactions(vehicule_id, event, transactions)            # APPEL DE LA FONCTION SAUVEGARDER TRANSACTION ( dans crud.py)
                        sleep(0.5)

                    case Etats.STATIONNEMENT:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        vert()
    # lancer les THREADS. "if not" pour le lancer slmt UNE fois
                        if not rappel_lance:                  # thread demarre  pour le rappel
                            threadRappel = threading.Thread(target=envoyer_rappel)
                            threadRappel.start()
                            rappel_lance = True

                        if not notif_expire:  # thread demarre  pour l'expiration
                            threadTempsExpire = threading.Thread(target=temps_expire)
                            threadTempsExpire.start()
                            notif_expire = True

                        event = getEvent(etat, etat_precedent)
                        
                        sleep(0.5)

                    case Etats.ATTENTE_SORTIE:
                        vehicule_Id = sortir_vehicule(liste_vehicules)        # cette fonction (dans crud) identifie le vehicule avec le temps restant le plus petit
                        update_data(vehicule_id=vehicule_Id)    # ces deux lignes sont placées en premier pour s'updater avant le changement d'etat pour log et comm

                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)

                        stop_rappel.set()
                        stop_temps_expire.set()

                        try:
                            threadRappel.join()                         # termine le thread rappel
                            threadTempsExpire.join()                        # termine thread temps expire
                        except NameError:
                            pass

                        rappel_lance = False    # eviter que le rappel se lance a nouveau
                        notif_expire = False
                        barriere_ouvert()
                        barriere_ferme()
                        jaune()
                    # preparer les variables pour les garder dans sauvegarder_ transactions ( dans crud.py )

                        event = Event.DETECTE_SORTIE_TICKET
                        sauvegarder_transactions(vehicule_Id, event, transactions)
                        sleep(0.5)
                        supprimer_vehicule(sortir_vehicule(liste_vehicules))   # dans crud.py.  maintenant que la transaction est faite, on peut supprimer le vehicule                    
                        sleep(0.5)

                    case Etats.ERREUR:
                        etat, etat_precedent = eviter_surcharge_etat(etat, etat_precedent)
                        rouge()
                        buzzer_alarme()
                        event = getEvent(etat, etat_precedent)
                        sleep(0.5)

                
                # if not verifier_ecran():
                #     break

                sleep(0.1)


            except Exception as e: # Gestion des erreurs, log et envoie en etat d'erreur
                print(e)
                
                logerreur(e)  
                event= Event.ERREUR 
            
                

    except KeyboardInterrupt:
        print("Programme arrete")
                 
    finally:
        pass

if __name__ ==  "__main__":
    parking_system()
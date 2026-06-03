import smtplib
from time import time                  
from config.config_loader import sender_email, app_password, recipient_email
from config.logsconfig import logEmail, logerreur
from models.vehicle import liste_vehicules, charger
from models.parking import get_data, update_data
from datetime import datetime



def sendEmail(etat, event):
    try:
        current_time = int(time())  # Recuperation des donnees pour la creation de messages
        shared = get_data()
        liste = charger()
        vehiculeID = shared["vehicule_id"]

        for veh in liste:
            if veh["vehicule_id"] == vehiculeID or vehiculeID == None:
                vehiculeID = veh["vehicule_id"]
                H_arrive = veh["heure_arrivee"]
                H_depart = veh["heure_depart"]
                Duree = veh["duree"]
                calcul_duree = H_arrive+Duree
                calcul_duree_reel=H_depart-H_arrive
                if calcul_duree_reel > Duree:
                    depassement = calcul_duree_reel - Duree
                Heure_arrive = datetime.fromtimestamp(H_arrive)     #  Differents calculs pour le bon affichage des heures et du temps
                Heure_prevue = datetime.fromtimestamp(calcul_duree)
                Heure_depart = datetime.fromtimestamp(H_depart)
                temps_duree_reel= int(calcul_duree_reel)
                temps_depassement=int(depassement) 
                duree_affiche = int(Duree/10)  
                
                match event:
                    case "Vehicule enregistre, ticket fourni":  # Se retrouve dans utils
                        subject = "Bienvenue au parking OZ'Anchois"
                        body = f"Pour le vehicule : {vehiculeID}\nVotre Heure d'arrivee est : {Heure_arrive}\nVous avex selectionne une duree de : {duree_affiche}H\nVous etes suppose partie avant : {Heure_prevue}"
                        send_email(subject,body)

                    case "Le stationnement est plein":  #  se retrouve dans main 
                        subject = "Parking complet "
                        body = f"Le parking est actuellement plein. Merci de revenir plus tard."
                        send_email(subject,body)

                match etat:
                    case "STATIONNEMENT" | "IDLE":  #  se retrouve dans main 
                        subject = "Votre reservation expire bientot "
                        body = f"Vous avez 2,5 secondes reelles (15 min simulees) pour quitter le parking."
                        send_email(subject,body)
                    

                    case "ATTENTE SORTIE": # Se retrouve dans utils
                        subject = "Merci, au revoir !"
                        body = f"Pour le vehicule : {vehiculeID}\nVous avez quitte a : {Heure_depart}\nVous etes reste : {temps_duree_reel}H\nVous avez depasse de :  {temps_depassement}H"
                        send_email(subject,body)

    except Exception as e: # Gestion des erreurs, log 
        print(e)
        logerreur(e) 
        return


def send_email(subject,body):
    message=f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(user=sender_email, password=app_password)
        connection.sendmail(from_addr=sender_email,
                            to_addrs=recipient_email,
                            msg=message)
    recipient = recipient_email
    logEmail(recipient)
    







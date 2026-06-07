import logging
from models.parking import get_data
from models.state_machine import Etats
from config.config_loader import LOG_FILE, LOG_LEVEL, CAPACITE_MAX

#logs
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s'
)

# Logs relié a evenements -- se retrouve dans utils  
def logevent(event):

        # messages des log d'evenements
    shared = get_data()
    nbplace = shared["places"]
    etat = shared["etat"]
    
    message_entree = "Un vehicule est entre dans le stationnement"
    message_sortie = "Un vehicule est sorti du stationnement"
    message_detection = "Un vehicule a ete detecte a l'entree du stationnement"
    message_nbplace = f"Nb de place restantes : {nbplace} /{CAPACITE_MAX}"
    message_code_errone = f"Un Mauvais code {etat} a ete saisi"
    message_code_superadmin = "UN CODE SUPERADMIN ERRONE A ETE SAISI"
   

    match event:
        case "Vehicule detecte":
            logging.info(message_detection)

        case "Vehicule enregistre, ticket fourni":
            logging.info(message_entree)
            logging.info(message_nbplace)

        case "vehicule sorti":
            shared = get_data()
            nbplace = shared["places"]
            logging.info(message_sortie)
            logging.info(message_nbplace)

        case "ECHEC D'AUTHENTIFICATION":
            logging.info(message_code_errone)

        case "AUTHENTIFICATION SUPERADMIN":
            logging.info(message_code_superadmin)
        

# Log des changements d'etats -- se retrouve dans utils
def logchetat(etat,etat_precedent):
    message_fermeture = f"Le Parking a ete ferme"
    message_ouverture = f"Le Parking est ouvert"
    message_erreur =f"Vous etes sorti de l'etat d'erreur"
    message_superadmin =f"Un SUPERADMIN a ete necessaire pour sortir de ce pepin"
    if isinstance(etat,  Etats):        # verifie les enums pour associer aux values 
        etat = etat.value
    if isinstance(etat_precedent,  Etats):      # verifie les enums pour associer aux values.  l'etat precedent n'avait pas d'enum mais il peut se comparer a l'enum Etats 
        etat_precedent = etat_precedent.value
    message_ch_etat = (f"Changement d'etat : {etat_precedent} ---> {etat}")
    logging.info(message_ch_etat)
    match etat, etat_precedent:
        case "IDLE","ADMINISTRATEUR":
            logging.info(message_ouverture)
        case "FERME","ADMINISTRATEUR":
            logging.info(message_fermeture)
        case "IDLE","SUPER ADMINISTRATEUR":
            logging.info(message_superadmin)
        case "IDLE","USAGER":
            logging.info(message_erreur)
           

    

def logapi(e): # logs relié a l'API etat de connection et erreurs -- se retrouve dans api
    if e == "connecte":
        logging.info(f"API bien connecte")
    else:
        logging.error(f"Une erreur API est survenue:\n{e}", stacklevel=3)


def logerreur(erreur):      # Log d'erreur general -- se retrouve dans main
    logging.error(f"Une erreur est survenue:\n{erreur}", stacklevel=3)  # remonte de 3 le chemin de l'erreur.. on peut l'augmenter au choix

def logEmail(recipient):    # se trouve dans comm
    logging.info(f'Un courriel a été envoyé a {recipient}')

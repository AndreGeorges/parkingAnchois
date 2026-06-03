import logging
from models.parking import get_data
from models.state_machine import Etats

#logs
logging.basicConfig(
    filename='logs/parking.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s'
)

# Logs relié a evenements -- se retrouve dans utils  
def logevent(event):

        # messages des log d'evenements
    shared = get_data()
    nbplace = shared["places"]
    
    message_entree = "Un vehicule est entre dans le stationnement"
    message_sortie = "Un vehicule est sorti du stationnement"
    message_detection = "Un vehicule a ete detecte a l'entree du stationnement"
    message_nbplace = f"Nb de place restantes : {nbplace} /5"

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

# Log des changements d'etats -- se retrouve dans utils
def logchetat(etat,etat_precedent):
    if isinstance(etat,  Etats):        # verifie les enums pour associer aux values 
        etat = etat.value
    if isinstance(etat_precedent,  Etats):      # verifie les enums pour associer aux values.  l'etat precedent n'avait pas d'enum mais il peut se comparer a l'enum Etats 
        etat_precedent = etat_precedent.value
    message_ch_etat = (f"Changement d'etat : {etat_precedent} ---> {etat}")
    logging.info(message_ch_etat)
    

def logapi(e): # logs relié a l'API etat de connection et erreurs -- se retrouve dans api
    if e == "connecte":
        logging.info(f"API bien connecte")
    else:
        logging.error(f"Une erreur API est survenue:\n{e}", stacklevel=3)


def logerreur(erreur):      # Log d'erreur general -- se retrouve dans main
    logging.error(f"Une erreur est survenue:\n{erreur}", stacklevel=3)  # remonte de 3 le chemin de l'erreur.. on peut l'augmenter au choix

def logEmail(recipient):    # se trouve dans comm
    logging.info(f'Un courriel a été envoyé a {recipient}')

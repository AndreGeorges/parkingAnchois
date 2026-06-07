from config.config_loader import TARIFS, SCREEN_COLOR, COLOR
from models.logger_manager import logchetat, logevent
from services.email_service import sendEmail



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

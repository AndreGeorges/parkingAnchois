from enum import Enum


class Etats(Enum):
    IDLE = "IDLE"
    FERME = "FERME"
    ATTENTE_ENTREE = "ATTENTE ENTREE"
    PAIEMENT_ENTREE = "PAIEMENT ENTREE"
    ACCES_ACCEPTE = "ACCES ACCEPTE"
    STATIONNEMENT = "STATIONNEMENT"
    ATTENTE_SORTIE = "ATTENTE SORTIE"
    ERREUR = "ERREUR"
    AUTH_ADMIN = "ADMINISTRATEUR"
    AUTH_SUPERADMIN = "SUPER ADMIN"
    AUTH_USAGER = "USAGER"
    
class Event(Enum):
    DEFAULT = "defaut"
    VEHICULE_DETECTE = "Vehicule detecte"
    PLACE_DISPONIBLE = "Place disponible"
    PLACE_INDISPONIBLE = "Le stationnement est plein"
    DUREE = 0
    DUREE_PAIEMENT_EFFECTUE = "Duree et paiement effectues"
    BARRIERE_ENREGISTREMENT_TICKET  = "Vehicule enregistre, ticket fourni"
    DEMANDE_SORTIE = "Sortie demandee"
    DETECTE_SORTIE_TICKET = "vehicule sorti"
    ANNULATION = "transaction annulee"
    ERREUR = "Erreur"
    RETOUR_IDLE = "Retour a idle"
    FERME = "Ferme"
    DEMANDE_AUTH_ADMIN = "AUTHENTIFICATION ADMIN"
    AUTH_ECHEC = "ECHEC D'AUTHENTIFICATION"
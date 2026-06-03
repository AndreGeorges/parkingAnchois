from config.config_loader import TARIFS, SCREEN_COLOR, COLOR


def get_tarif(duree, TARIFS):
    return TARIFS.get(duree)

def get_screen_color(etat_pg, SCREEN_COLOR):
    return SCREEN_COLOR.get(etat_pg)

# cette fonction permet de retourner la couleur
def get_color(color_name):
    return COLOR[color_name]
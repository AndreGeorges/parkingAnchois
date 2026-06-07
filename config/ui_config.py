from config.config_loader import TARIFS, SCREEN_COLOR, COLOR, AUTH_VIEW


def get_tarif(duree, TARIFS):
    return TARIFS.get(duree)

def get_screen_color(etat_pg, SCREEN_COLOR):
    return SCREEN_COLOR.get(etat_pg)

# cette fonction permet de retourner la couleur
def get_color(color_name):
    return COLOR[color_name]

# pour transformer le rgb en hexadecimal pour que tkinter comprenne la couleur
def get_color_rgb(color_name):
    rgb = COLOR[color_name]
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

# J'aurais surement pu juste passer par config_loader.. but here we are......
def get_AUTH():
    return AUTH_VIEW
from datetime import datetime

def exporter_log():  # Fonction appelée par pygame pour exporter les log et créer un nouveau fichier vide
    fichier = open("logs/parking.log","r")
    contenu = fichier.read()
    if contenu == "":           # Verifie qu'il n'envoie pas un fichier vide.  si c'est le cas, aucun fichier n'est créé
        print("Aucun fichier a archiver")
        fichier.close()
        return
    date = datetime.now().strftime("%Y%m%dT%H%M%S") # format de date YYYYMMDDTHHMMSS
    nouveau_fichier =open(f"exports/{date}.log","w")
    nouveau_fichier.write(contenu)
    nouveau_fichier.close()
    fichier.close()
    fichier = open("logs/parking.log","w") # Crée le nouveau fichier vide
    fichier.close()
    print("Log Exporte")

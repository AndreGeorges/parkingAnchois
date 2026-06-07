from datetime import datetime

def exporter_log():
    fichier = open("logs/parking.log","r")
    contenu = fichier.read()
    if contenu == "":
        print("Aucun fichier a archiver")
        fichier.close()
        return
    date = datetime.now().strftime("%Y%m%dT%H%M%S")
    nouveau_fichier =open(f"exports/{date}.log","w")
    nouveau_fichier.write(contenu)
    nouveau_fichier.close()
    fichier.close()
    fichier = open("logs/parking.log","w")
    fichier.close()
    print("Log Exporte")

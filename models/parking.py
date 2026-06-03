import threading
lock=threading.Lock()
data= {
"etat": "IDLE",
"event": "defaut", 
"places": 5,
"tarif": 0,
"vehicule_id": None,
"file_attente": "",
"historique": "",
"transactions" : "",
"message": "",
"user_input": "",
"input_ready": False,
"keyboard":False
}
# cette fonction recupere les variables utilisees dans le main (apres le while True)
def update_data(**kwargs):    # **kwargs permet de recevoir un nombre variable d’arguments nommés dans une fonction.
    with lock:           # verouille momentanement l'acces au dictionnaire
        data.update(kwargs)

# recupere une copie des donnees partagees entre THREADS
def get_data():
    with lock:
        return data.copy()
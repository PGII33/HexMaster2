""" Fichier principal du jeu """

import sys
from src.app.application import Application

if __name__ == '__main__':
    args = sys.argv

    mode = sys.argv[1] if len(sys.argv) > 1 else "accueil"
    if mode == "demo":
        Application("demo").lancer()
    elif mode in ["playground", "bac_a_sable"]:
        Application("playground").lancer()
    elif mode in ["accueil", "parametres"]:
        Application(mode).lancer()
    else:
        print(f"Mode '{mode}' non reconnu. Utilisez 'demo', 'playground', 'accueil' ou 'parametres'.")
        sys.exit(1)

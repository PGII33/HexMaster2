""" Fichier principal du jeu """

import sys
from src.app.application import Application

if __name__ == '__main__':
    args = sys.argv

    mode = sys.argv[1] if len(sys.argv) > 1 else "accueil"
    if mode in ["demo", "playground", "accueil", "parametres", "credits"]:
        Application(mode).lancer()
    else:
        print(f"Mode '{mode}' non reconnu. Utilisez 'demo', 'playground', 'accueil', 'parametres' ou 'credits'.")
        sys.exit(1)

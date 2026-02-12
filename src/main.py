""" Fichier principal du jeu """

import sys
from src.demo import demo
from src.playground import playground
from src.affichage.vue_jeu import VueJeu

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        print("Usage: python main.py [demo|playground]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "demo":
        vue = VueJeu(demo)
        vue.lancer()
    elif mode == "playground":
        vue = VueJeu(playground)
        vue.lancer()

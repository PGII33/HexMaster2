""" Fichier principal du jeu """

import sys
from src.demo import creer_demo
from src.playground import creer_playground
from src.affichage.vue_jeu import VueJeu

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        print("Usage: python main.py [demo|playground]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "demo":
        demo = creer_demo()
        vue = VueJeu(demo)
        vue.lancer()
    elif mode == "playground":
        playground = creer_playground()
        vue = VueJeu(playground)
        vue.lancer()

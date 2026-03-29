""" Fichier de l'écran de jeu, qui affiche le plateau et gère les interactions pendant la partie """

from src.app.ecrans.base_ecran import BaseEcran
from src.affichage.vue_jeu import VueJeu

class EcranJeu(BaseEcran):
    """ Ecran du jeu """
    def __init__(self, width, height, jeu):
        super().__init__(width, height)
        self.vue_jeu = VueJeu(jeu, width, height)

    def handle_events(self, events):
        self.vue_jeu.handle_events(events)
        if not self.vue_jeu.running:
            self.set_prochain_ecran("accueil")
    
    def update(self, dt):
        self.vue_jeu.update(dt)
    
    def afficher(self, surface):
        self.vue_jeu.afficher(surface)
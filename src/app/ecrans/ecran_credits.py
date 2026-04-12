""" Ecran des crédits du jeu """

import pygame
from . import const as c
from src.app.ecrans.base_ecran import BaseEcran
from ..ui.bouton_hex import BoutonHex

class EcranCredits(BaseEcran):
    """ Ecran des crédits du jeu"""
    def __init__(self, width:int, height:int, son_manager=None):
        super().__init__(width, height, son_manager)
        pygame.font.init()
        self._font = pygame.font.Font(None, c.FONT_SIZE)

        self._boutons = []
        self._boutons.append(BoutonHex(int(self._width * 0.02), int(self._height * 0.02), 100, 40, "Retour", self._font, action="accueil"))


    def handle_events(self, events:list):
        """ Gérer les événements de l'écran des crédits"""
        for event in events:
            for bouton in self._boutons:
                if bouton.handle_event(event):
                    action: str|None = bouton.get_action()
                    if action:
                        if self._son_manager and self._son_manager.get_son("ui_click"):
                            self._son_manager.jouer_son("ui_click")
                        self.set_prochain_ecran(action)

    def afficher(self, surface):
        """ Afficher l'écran des crédits sur la surface donnée"""
        surface.fill(c.GRIS_CLAIR)
        for bouton in self._boutons:
            bouton.afficher(surface)

    def update(self, dt):
        """ Mettre à jour l'état de l'écran des crédits"""
        for bouton in self._boutons:
            bouton.update(dt, pygame.mouse.get_pos())
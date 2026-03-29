""" Ecran d'acceuil du jeu """

import pygame
from . import const as c
from src.app.ecrans.base_ecran import BaseEcran
from ..ui.bouton_hex import BoutonHex


class EcranAccueil(BaseEcran):
    """ Ecran d'acceuil du jeu"""
    def __init__(self, width:int, height:int):
        super().__init__(width, height)
        pygame.font.init()
        self._font = pygame.font.Font(None, c.FONT_SIZE)
        self._texte_titre = self._font.render("HexMaster 2", True, (c.NOIR))

        self._boutons = []

        self._boutons.append(BoutonHex(self._width // 2 - 100, int(self._height * 0.4), 200, 50, "Démo", self._font, action="demo"))
        self._boutons.append(BoutonHex(self._width // 2 - 100, int(self._height * 0.5), 200, 50, "Bac à sable", self._font, action="bac_a_sable"))
        self._boutons.append(BoutonHex(self._width // 2 - 100, int(self._height * 0.6), 200, 50, "Paramètres", self._font, action="parametres"))


    def handle_events(self, events:list):
        """ Gérer les événements de l'écran d'accueil"""
        for event in events:
            for bouton in self._boutons:
                if bouton.handle_event(event):
                    action: str|None = bouton.get_action()
                    if action:
                        self.set_prochain_ecran(action)


    def afficher(self, surface):
        """ Afficher l'écran d'accueil sur la surface donnée"""
        surface.fill(c.GRIS_CLAIR)

        for bouton in self._boutons:
            bouton.afficher(surface)

    def update(self, dt):
        """ Mettre à jour l'état de l'écran d'accueil"""
        for bouton in self._boutons:
            bouton.update(dt, pygame.mouse.get_pos())
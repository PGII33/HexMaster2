""" Ecran des paramètres du jeu """

import pygame
from . import const as c
from src.app.ecrans.base_ecran import BaseEcran
from ..ui.bouton_hex import BoutonHex
from ..ui.slider import Slider

class EcranParametres(BaseEcran):
    """ Ecran des paramètres du jeu"""
    def __init__(self, width:int, height:int, son_manager=None):
        super().__init__(width, height, son_manager)
        pygame.font.init()
        self._font = pygame.font.Font(None, c.FONT_SIZE)

        self._boutons = []
        self._boutons.append(BoutonHex(int(self._width * 0.02), int(self._height * 0.02), 100, 40, "Retour", self._font, action="accueil"))

        self._sliders = []
        self._sliders.append(Slider(int(self._width * 0.1), int(self._height * 0.2), int(self._width * 0.4), 20, min_value=0.0, max_value=1.0, initial_value=son_manager.get_volume_global()))
        self._sliders.append(Slider(int(self._width * 0.1), int(self._height * 0.3), int(self._width * 0.4), 20, min_value=0.0, max_value=1.0, initial_value=son_manager.get_volume_sfx()))
        self._sliders.append(Slider(int(self._width * 0.1), int(self._height * 0.4), int(self._width * 0.4), 20, min_value=0.0, max_value=1.0, initial_value=son_manager.get_volume_musique()))

    def handle_events(self, events:list):
        """ Gérer les événements de l'écran des paramètres"""
        for event in events:
            for bouton in self._boutons:
                if bouton.handle_event(event):
                    action: str|None = bouton.get_action()
                    if action:
                        if self._son_manager and self._son_manager.get_son("ui_click"):
                            self._son_manager.jouer_son("ui_click")
                        self.set_prochain_ecran(action)
            if self._sliders[0].handle_event(event):
                new_volume = round(self._sliders[0].get_value(), 3)
                if self._son_manager:
                    self._son_manager.set_volume_global(new_volume)
            if self._sliders[1].handle_event(event):
                new_volume = round(self._sliders[1].get_value(), 3)
                if self._son_manager:
                    self._son_manager.set_volume_sfx(new_volume)
            if self._sliders[2].handle_event(event):
                new_volume = round(self._sliders[2].get_value(), 3)
                if self._son_manager:
                    self._son_manager.set_volume_musique(new_volume)


    def afficher(self, surface):
        """ Afficher l'écran des paramètres sur la surface donnée"""
        surface.fill(c.GRIS_CLAIR)
        for bouton in self._boutons:
            bouton.afficher(surface)
        for slider in self._sliders:
            slider.afficher(surface)

    def update(self, dt):
        """ Mettre à jour l'état de l'écran des paramètres"""
        for bouton in self._boutons:
            bouton.update(dt, pygame.mouse.get_pos())
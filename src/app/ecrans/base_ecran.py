""" Fichier de la classe abstraite BaseEcran"""
from abc import ABC, abstractmethod

class BaseEcran(ABC):
    """ Classe abstraite pour les écrans du jeu"""
    def __init__(self, width:int, height:int):
        self._width = width
        self._height = height
        self._prochain_ecran: str|None = None  # prochain ecran à afficher parmi [accueil, parametres, demo, playground, quit]

    def set_prochain_ecran(self, ecran:str|None)-> None:
        """ Définir le prochain écran à afficher"""
        self._prochain_ecran = ecran
    
    def get_prochain_ecran(self) -> str|None:
        """ Obtenir le prochain écran à afficher"""
        return self._prochain_ecran

    @abstractmethod
    def handle_events(self, events:list):
        """ Gérer les événements de l'écran"""
        pass

    @abstractmethod
    def afficher(self, surface):
        """ Afficher l'écran sur la surface donnée"""
        pass

    @abstractmethod
    def update(self, dt):
        """ Mettre à jour l'état de l'écran"""
        pass

    def transition(self):
        """ Retourner le prochain écran à afficher, ou None pour rester sur le même"""
        ecran: str|None = self.get_prochain_ecran()
        self.set_prochain_ecran(None)
        return ecran

    def on_enter(self):
        """ Appelé lorsque l'écran devient actif"""
        pass

    def on_exit(self):
        """ Appelé lorsque l'écran devient inactif"""
        pass


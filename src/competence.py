""" Fichier de gestion des effets """
from src.phase import PhaseTour
from src.effet import Effet

class Competence:
    """ Base de tous les effets du jeu """
    def __init__(self, duree:int, phase:PhaseTour, effet:Effet):
        """ Initialise l'effet """
        self.duree = duree
        self.phase = phase
        self.effet = effet

    def get_duree(self):
        """ Retourne la duree de l'effet """
        return self.duree

    def get_phase(self):
        """ Retourne la phase de l'effet """
        return self.phase

    def get_effet(self):
        """ Retourne l'effet """
        return self.effet

    def appliquer_effet(self, origine, toutes_entitees):
        """ Applique l'effet """
        self.effet(origine, toutes_entitees)

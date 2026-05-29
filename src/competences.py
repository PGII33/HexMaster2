""" Fichier de gestion des effets """
from src.phase import PhaseTour
from src.effets import Effet


class Competence:
    """ Base de tous les effets du jeu """

    def __init__(self, duree: int, phase: PhaseTour, nom_effet: str):
        """ Initialise l'effet """
        self.duree = duree
        self.phase = phase
        self.nom_effet = nom_effet

    def get_duree(self):
        """ Retourne la duree de l'effet """
        return self.duree

    def get_phase(self):
        """ Retourne la phase de l'effet """
        return self.phase

    def appliquer_effet(self, origine, toutes_entitees, cible=None, joueurs=None):
        """ Applique l'effet

        Args:
            origine: L'entité qui possède la compétence
            toutes_entitees: Liste de toutes les entités du terrain
            cible: Cible de l'effet (optionnel)
            joueurs: Dictionnaire {numero_equipe: objet_joueur} (optionnel)
        """
        Effet.appliquer_nom(self.nom_effet, origine, toutes_entitees, cible, joueurs)

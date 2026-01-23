""" Fichier de gestion des Entites """

from src.competence import Competence
from src.base import Base

class Entite(Base):
    """ Base de toutes les entites du jeu """
    def __init__(self, pv:int, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, combat:int, demolition:int, degradation:int,
                 portee:int, control:int, comp:list[Competence]=None):
        """ Initialise l'entite """
        super().__init__(nom=nom, pos=pos, cout=cout,equipe=equipe, combat=combat,
                         demolition=demolition, degradation=degradation, portee=portee,
                         comp=comp)
        self.en_vie = True
        self.pv = pv
        self.control = control

    def print(self):
        """ Affiche les informations de l'entite """
        print(f"Entite: {self.nom}, PV: {self.pv}, Cout: {self.cout}")

    def est_en_vie(self):
        """ Retourne la valeur de l'attribut en_vie """
        return self.en_vie

    def get_pv(self):
        """ Retourne les points de vie de l'entite """
        return self.pv

    def get_control(self):
        """ Retourne la valeur de l'attribut control """
        return self.control

    def set_en_vie(self, valeur:bool):
        """ Modifie l'attribut en_vie """
        self.en_vie = valeur

    def set_pv(self, pv:int):
        """ Modifie les points de vie de l'entite """
        self.pv = pv

    def set_control(self, control:int):
        """ Modifie l'attribut control """
        self.control = control

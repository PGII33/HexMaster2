""" Fichier de gestion de Entite """

from src.competences import Competence
from src.base import Base

class Entite(Base):
    """ Classe de entite, la base avec de combats, démolition, dégradation et portée """
    def __init__(self, pv:int, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, control:int, comp:list[Competence]=None, sprite_path:str=None,
                 carte_path:str=None):
        """ Initialise la base """
        super().__init__(nom, pos, cout, equipe, comp, sprite_path, carte_path)
        self.pv = pv
        self.control = control

    def get_pv(self):
        """ Retourne les points de vie de l'entite """
        return self.pv

    def set_pv(self, pv:int):
        """ Modifie les points de vie de l'entite """
        self.pv = pv

    def get_control(self):
        """ Retourne la valeur de l'attribut control """
        return self.control

    def set_control(self, control:int):
        """ Modifie l'attribut control """
        self.control = control

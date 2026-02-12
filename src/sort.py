""" Fichier de gestion des sorts """
from typing_extensions import override
from src.competence import Competence
from src.base import Base

class Sort(Base):
    """ Classe representant un sort """
    def __init__(self, nom:str, pos:tuple[int, int], cout:int, equipe:int,
                 comp:Competence, sprite_path:str=None, carte_path:str=None):
        """ Initialise le sort """
        super().__init__(nom=nom, pos=pos, cout=cout,
                         equipe=equipe, comp=comp, sprite_path=sprite_path,
                         carte_path=carte_path)

    @override
    def est_sort(self):
        """ Retourne vrai si l'entite est un sort """
        return True

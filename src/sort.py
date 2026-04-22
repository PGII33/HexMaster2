""" Fichier de gestion des sorts """

from __future__ import annotations
from typing_extensions import override
from src.competences import Competence
from src.base import Base

class Sort(Base):
    """ Classe representant un sort """
    def __init__(self, nom:str, pos:tuple[int, int], cout:int, equipe:int,
                 comp:list[Competence], tags:list[Tag]=None, sprite_path:str=None, carte_path:str=None):
        """ Initialise le sort """
        super().__init__(nom=nom, pos=pos, cout=cout,
                         equipe=equipe, comp=comp, tags=tags, sprite_path=sprite_path,
                         carte_path=carte_path)

    @override
    def est_sort(self):
        """ Retourne vrai si l'entite est un sort """
        return True

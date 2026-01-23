""" Fichier de gestion des sorts """
from typing_extensions import override
from src.competence import Competence
from src.base import Base

class Sort(Base):
    """ Classe representant un sort """
    def __init__(self, nom:str, pos:tuple[int, int], cout:int, equipe:int,
                 combat:int, demolition:int, degradation:int, portee:int,
                 comp:Competence):
        """ Initialise le sort """
        super().__init__(nom=nom, pos=pos, cout=cout,
                         equipe=equipe, combat=combat, demolition=demolition,
                         degradation=degradation, portee=portee, comp=comp)

    @override
    def est_sort(self):
        """ Retourne vrai si l'entite est un sort """
        return True

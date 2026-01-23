""" Fichier de gestion des Batiments """
from typing_extensions import override
from src.entite import Entite
from src.competence import Competence

class Batiment(Entite):
    """ Batiment du jeu """
    def __init__(self, pv:int, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, combat: int, demolition: int, degradation: int,
                 portee:int, control:int, comp:list[Competence]=None):
        """ Initialise le batiment """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                         combat=combat, demolition=demolition, degradation=degradation,
                         portee=portee, control=control, comp=comp)

    @override
    def est_batiment(self):
        """ Retourne vrai si l'entite est un batiment """
        return True

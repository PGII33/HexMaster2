""" Fichier de gestion des creatures """
from typing_extensions import override
from src.entite import Entite
from src.competence import Competence

class Creature(Entite):
    """ Creature du jeu """
    def __init__(self, pv:int, nom:str, cout:int, pos:tuple[int, int],
                 equipe:int, combat: int, demolition: int, degradation: int,
                 portee:int, control:int, mouv:int, Comp:list[Competence]=None):
        """ Initialise la creature """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                         combat=combat, demolition=demolition, degradation=degradation,
                         control=control, portee=portee, comp=Comp)
        self.mouv = mouv # Points de mouvements

    def __str__(self):
        """ Représentation en chaîne de caractères """
        return f"Creature: {self.nom} (Pos: {self.pos}, PV: {self.pv}, Cout: {self.cout}, Equipe: {self.equipe}, Mouv: {self.mouv})"

    def get_mouv(self):
        """ Retourne les points de mouvement de l'unite """
        return self.mouv

    def set_mouv(self, mouv:int):
        """ Modifie les points de mouvement de l'unite """
        self.mouv = mouv

    @override
    def est_creature(self):
        """ Retourne vrai si l'entite est une creature """
        return True

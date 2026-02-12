""" Fichier de gestion des Unite """

from src.competence import Competence
from src.entite import Entite
from src.auxliaire import est_a_portee_hex

class Unite(Entite):
    """ Base de toutes les unites du jeu """
    def __init__(self, pv:int, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, combat:int, demolition:int, degradation:int,
                 portee:int, control:int, comp:list[Competence]=None, sprite_path:str=None,
                 carte_path:str=None):
        """ Initialise l'unite """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout,equipe=equipe,
                         control=control,
                         comp=comp, sprite_path=sprite_path, carte_path=carte_path)
        self.combat = combat
        self.demolition = demolition
        self.degradation = degradation
        self.portee = portee
        self.a_attaque = False

    def get_portee(self):
        """ retourne la portée """
        return self.portee

    def set_portee(self, portee:int):
        """ Modifie la portée """
        self.portee = portee

    def get_combat(self):
        """ Retourne la valeur de combat """
        return self.combat

    def set_combat(self, combat:int):
        """ Modifie la valeur de combat """
        self.combat = combat

    def get_demolition(self):
        """ Retourne la valeur de demolition """
        return self.demolition

    def set_demolition(self, demolition:int):
        """ Modifie la valeur de demolition """
        self.demolition = demolition

    def get_degradation(self):
        """ Retourne la valeur de degradation """
        return self.degradation

    def set_degradation(self, degradation:int):
        """ Modifie la valeur de degradation """
        self.degradation = degradation

    def get_a_attaque(self):
        """ Retourne si l'unité a déjà attaqué ce tour """
        return self.a_attaque

    def set_a_attaque(self, valeur: bool):
        """ Modifie l'attribut a_attaque """
        self.a_attaque = valeur

    def fin_tour(self):
        """ Comportement de fin de tour """
        self.a_attaque = False

# Actions

    def attaquer(self, cible):
        """ Attaque une cible """
        if not est_a_portee_hex(self.pos, cible.get_pos(), self.portee):
            return
        if cible.est_creature():
            cible.set_pv(cible.get_pv() - self.get_combat())
        elif cible.est_batiment():
            cible.set_pv(cible.get_pv() - self.get_demolition())
        elif cible.est_case():
            cible.set_pv(cible.get_pv() - self.get_degradation())

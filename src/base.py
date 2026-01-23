""" Fichier de gestion de base """

from src.competence import Competence
from src.phase import PhaseTour

class Base:
    """ Classe de base """
    def __init__(self, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, combat:int, demolition:int, degradation:int,
                 portee:int, comp:list[Competence]=None):
        """ Initialise la base """
        self.nom = nom
        self.pos = pos
        self.cout = cout
        self.equipe = equipe
        self.combat = combat
        self.demolition = demolition
        self.degradation = degradation
        self.portee = portee
        self.comp = comp if comp is not None else []

    def __str__(self):
        """ Représentation en chaîne de caractères """
        return f"{self.nom} (Pos: {self.pos}, Cout: {self.cout}, Equipe: {self.equipe})"

    def get_nom(self):
        """ Retourne le nom """
        return self.nom

    def get_pos(self):
        """ Retourne la position axiale """
        return self.pos

    def get_cout(self):
        """ Retourne le cout """
        return self.cout

    def get_portee(self):
        """ retourne la portée """
        return self.portee

    def get_equipe(self):
        """ Retourne l'equipe """
        return self.equipe

    def get_combat(self):
        """ Retourne la valeur de combat """
        return self.combat

    def get_demolition(self):
        """ Retourne la valeur de demolition """
        return self.demolition

    def get_degradation(self):
        """ Retourne la valeur de degradation """
        return self.degradation

    def get_comp(self):
        """ Retourne les competences """
        return self.comp

    def set_nom(self, nom:str):
        """ Modifie le nom """
        self.nom = nom

    def set_pos(self, pos:tuple[int, int]):
        """ Modifie la position axiale """
        self.pos = pos

    def set_cout(self, cout:int):
        """ Modifie le cout """
        self.cout = cout

    def set_portee(self, portee:int):
        """ Modifie la portée """
        self.portee = portee

    def set_equipe(self, equipe:int):
        """ Modifie l'equipe """
        self.equipe = equipe

    def set_combat(self, combat:int):
        """ Modifie la valeur de combat """
        self.combat = combat

    def set_demolition(self, demolition:int):
        """ Modifie la valeur de demolition """
        self.demolition = demolition

    def set_degradation(self, degradation:int):
        """ Modifie la valeur de degradation """
        self.degradation = degradation

    def set_comp(self, comp:list[Competence]):
        """ Modifie les competences """
        self.comp = comp

    def ajouter_competence(self, comp:Competence):
        """ Ajoute une competence """
        self.comp.append(comp)

    def retirer_competence(self, comp:Competence):
        """ Retire une competence """
        if comp in self.comp:
            self.comp.remove(comp)

# Getters particuliers

    def est_creature(self):
        """ Retourne vrai si l'entite est une creature """
        return False

    def est_batiment(self):
        """ Retourne vrai si l'entite est un batiment """
        return False

    def est_sort(self):
        """ Retourne vrai si l'entite est un sort """
        return False

    def est_case(self):
        """ Retourne vrai si l'entite est une case """
        return False

# Actions

    def debut_tour(self):
        """ Actions a effectuer au debut du tour """
        for comp in self.comp:
            if comp.get_phase() ==  PhaseTour.DEBUT_TOUR:
                comp.appliquer_effet(self)

    def fin_tour(self):
        """ Actions a effectuer a la fin du tour """
        for comp in self.comp:
            if comp.get_phase() ==  PhaseTour.FIN_TOUR:
                comp.appliquer_effet(self)

    def avant_attaque(self):
        """ Actions a effectuer avant une attaque """

    def apres_attaque(self):
        """ Actions a effectuer apres une attaque """

    def attaquer(self, cible):
        """ Attaque une cible """
        self.avant_attaque()
        if cible.est_creature():
            cible.set_pv(cible.get_pv() - self.get_combat())
            if cible.get_pv() <= 0:
                cible.set_en_vie(False)
        elif cible.est_batiment():
            cible.set_pv(cible.get_pv() - self.get_demolition())
            if cible.get_pv() <= 0:
                cible.set_en_vie(False)
        elif cible.est_case():
            cible.set_pv(cible.get_pv() - self.get_degradation())
            if cible.get_pv() <= 0:
                cible.set_en_vie(False)
        self.apres_attaque()

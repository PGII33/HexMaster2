""" Fichier de gestion des Cases """
from typing_extensions import override
from src.entite import Entite
from src.competence import Competence

class Case(Entite):
    """ Case du jeu """
    def __init__(self, pv:int, nom:str, pos:tuple[int, int],
                 cout:int, equipe:int, combat:int, demolition:int,
                 degradation:int, portee:int, control:int, comp:list[Competence]=None):
        """ Initialise la case """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe, combat=combat,
                         demolition=demolition, degradation=degradation, control=control,
                         portee=portee, comp=comp)
        self.occupe = False # Indique si une unite est sur la case

    def __str__(self):
        """ Représentation en chaîne de caractères """
        return f"Case: {self.nom} (Pos: {self.pos}, PV: {self.pv}, Cout: {self.cout}, Equipe: {self.equipe})"

    def est_occupe(self):
        """ Retourne si la case est occupee """
        return self.occupe

    def set_occupe(self, valeur:bool):
        """ Modifie l'attribut occupe """
        self.occupe = valeur

    @override
    def est_case(self):
        """ Retourne vrai si l'entite est une case """
        return True

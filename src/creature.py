""" Fichier de gestion des creatures """
from typing_extensions import override
from src.unite import Unite
from src.competence import Competence


class Creature(Unite):
    """ Creature du jeu """

    def __init__(self, pv: int, nom: str, pos: tuple[int, int],
                 cout: int, equipe: int, combat: int, demolition: int,
                 degradation: int, portee: int, control: int, mouv: int,
                 comp: list[Competence] = None, sprite_path: str = None,
                 carte_path: str = None):
        """ Initialise la creature """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                         combat=combat, demolition=demolition, degradation=degradation,
                         control=control, portee=portee, comp=comp, sprite_path=sprite_path,
                         carte_path=carte_path)
        self.mouv = mouv  # Points de mouvements
        self.mouv_max = mouv  # Points de mouvements maximum
        self.mal_invocation = False  # True si vient d'être invoqué

    def get_mouv(self):
        """ Retourne les points de mouvement de l'unite """
        return self.mouv

    def set_mouv(self, mouv: int):
        """ Modifie les points de mouvement de l'unite """
        self.mouv = mouv

    def get_mal_invocation(self):
        """ Retourne la valeur de l'attribut mal_invocation """
        return self.mal_invocation

    def set_mal_invocation(self, valeur: bool):
        """ Modifie l'attribut mal_invocation """
        self.mal_invocation = valeur

    @override
    def est_creature(self):
        """ Retourne vrai si l'entite est une creature """
        return True

    @override
    def fin_tour(self):
        """ Réinitialise les mouvements et applique fin_tour de l'unite """
        super().fin_tour()
        self.mouv = self.mouv_max

    @override
    def debut_tour(self):
        """ Retire le mal d'invocation """
        self.mal_invocation = False  # Retire le mal d'invocation

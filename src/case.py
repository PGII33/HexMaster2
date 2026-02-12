""" Fichier de gestion des Cases """
from typing_extensions import override
from src.entite import Entite
from src.competence import Competence


class Case(Entite):
    """ Case du jeu """

    def __init__(self, pv: int, nom: str, pos: tuple[int, int],
                 cout: int, equipe: int, control_max: int, control:int=0,
                 comp: list[Competence] = None, sprite_path: str = None,
                 carte_path: str = None):
        """ Initialise la case """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                         control=control,
                         comp=comp, sprite_path=sprite_path,
                         carte_path=carte_path)
        self.control_max = control_max

    def get_control_max(self):
        """ Retourne la valeur maximale de control """
        return self.control_max

    def set_control_max(self, val: int):
        """ Modifie la valeur maximale de control """
        self.control_max = val

    @override
    def est_case(self):
        """ Retourne vrai si l'entite est une case """
        return True

    def appliquer_control(self, control_unite: int, equipe_unite: int):
        """ Applique le contrôle d'une unité sur cette case 

        Args:
            control_unite: Stat de control de l'unité
            equipe_unite: Équipe de l'unité (1, 2, etc.)
        """
        if self.equipe == equipe_unite:
            # Case déjà contrôlée par l'équipe : augmenter le control
            self.control = min(self.control + control_unite, self.control_max)
        else:
            # Case adverse ou neutre : tenter la capture
            if control_unite > self.control:
                # Capture réussie
                self.control = control_unite - self.control
                self.equipe = equipe_unite
            else:
                # Réduction du contrôle adverse
                self.control = self.control - control_unite

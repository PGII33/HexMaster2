""" Fichier de gestion des Bâtiments """
from typing_extensions import override
from src.unite import Unite
from src.competence import Competence


class Batiment(Unite):
    """ Bâtiment du jeu """

    def __init__(self, pv: int, nom: str, pos: tuple[int, int], cout: int,
                 equipe: int, combat: int, demolition: int, degradation: int,
                 portee: int, control: int, comp: list[Competence] = None, sprite_path: str = None,
                 carte_path: str = None):
        """ Initialise le bâtiment """
        super().__init__(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                         combat=combat, demolition=demolition, degradation=degradation,
                         portee=portee, control=control, comp=comp, sprite_path=sprite_path,
                         carte_path=carte_path)

    @override
    def est_batiment(self):
        """ Retourne vrai si l'entité est un bâtiment """
        return True

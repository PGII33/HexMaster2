""" Fichier principal du jeu """

from src.case import Case
from src.creature import Creature
from src.terrain import Terrain
from src.deck import Deck
from src.joueur import Joueur
from src.jeu import Classique

class CaseNeutre(Case):
    """ Classe représentant une case neutre """
    def __init__(self, pos:tuple[int, int], equipe:int):
        super().__init__(nom="Case Neutre", pos=pos, pv=10, cout=0, equipe=equipe,
                         combat=0, demolition=0, degradation=0, portee=0, control=5, comp=[])


class Paysan(Creature):
    """ Classe représentant une créature paysan """
    def __init__(self, pos:tuple[int, int], equipe:int):
        super().__init__(nom="Paysan", cout=1, pv=5,
                         combat=1, demolition=1, degradation=0, equipe=equipe, pos=pos,
                         portee=1, control=0, mouv=2)

posNeutre = [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (1, -1)]
posj1 = [(-2, 0), (-2, 1), (-2, 2), (-3, 1), (-3, 2)]
cNeutre = [CaseNeutre(x, 0) for x in posNeutre]
cj1 = [CaseNeutre(x, 1) for x in posj1]
cj2 = [CaseNeutre((-x[0], -x[1]), 2) for x in posj1]

case_demo = cNeutre + cj1 + cj2
terrain_demo = Terrain(case_demo)

deck_j1 = Deck([Paysan(None, 1) for _ in range(5)] + [CaseNeutre(None, 1) for _ in range(5)])
deck_j2 = Deck([Paysan(None, 2) for _ in range(5)] + [CaseNeutre(None, 2) for _ in range(5)])

deck_j1.melanger()
deck_j2.melanger()

j1 = Joueur(nom="Alice", deck=deck_j1, pi=5, numero=1)
j2 = Joueur(nom="Bob", deck=deck_j2, pi=5, numero=2)
demo = Classique([j1, j2], terrain_demo)

terrain_demo.print_entites()

demo.tour()

if __name__ == '__main__':
    print("Bienvenue dans HexMaster2 !")
    print("Le jeu est en cours de développement.")

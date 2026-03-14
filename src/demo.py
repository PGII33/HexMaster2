""" Démo du jeu """

from src.terrain import Terrain
from src.deck import Deck
from src.joueur import Joueur
from src.jeu import Classique
from src.chargeur.entite_chargeur import EntiteChargeur
from src.affichage.vue_jeu import VueJeu
from src.const import (
    PI_DEPART,
    NOMBRE_FERMIERS_DECK,
    NOMBRE_TERRAIN,
    NOMBRE_BUCHERON_DECK,
    NOMBRE_CHEVALIER_DECK,
    NOMBRE_ARCHERE_DECK,
    NOMBRE_PIQUES_DECK,
    NOMBRE_BARRIERES_DECK,
    TAILLE_MAIN_MAX
)

# Charger les entites
chargeur = EntiteChargeur()
chargeur.charger_toutes_les_entites()

# Terrain avec les cases
posNeutre = [(1, 0), (-1, 1), (-1, 0), (1, -1)]
posPiques = [(0, 0), (0, 1), (0, -1)]
posj1 = [(-2, 0), (-2, 1), (-2, 2), (-3, 1), (-3, 2)]

cNeutre = [chargeur.creer_instance("terrain", x, 0) for x in posNeutre]
cPiques = [chargeur.creer_instance("foret", x, 0) for x in posPiques]
cj1 = [chargeur.creer_instance("terrain", x, 1) for x in posj1]
cj2 = [chargeur.creer_instance(
    "terrain", (-x[0], -x[1]), 2) for x in posj1]

case_demo = cNeutre + cj1 + cj2 + cPiques
terrain_demo = Terrain(case_demo)

# Créer les decks avec des définitions (id, équipe)
deck_j1_definitions =[("archere", 1)] * NOMBRE_ARCHERE_DECK

deck_j2_definitions = [("fermier", 2)] * NOMBRE_FERMIERS_DECK + \
                      [("terrain", 2)] * NOMBRE_TERRAIN + \
                      [("bucheron", 2)] * NOMBRE_BUCHERON_DECK + \
                      [("chevalier", 2)] * NOMBRE_CHEVALIER_DECK + \
                      [("archere", 2)] * NOMBRE_ARCHERE_DECK + \
                      [("piques", 2)] * NOMBRE_PIQUES_DECK + \
                      [("pluie", 2)] * NOMBRE_BARRIERES_DECK

deck_j1 = Deck(deck_j1_definitions, chargeur)
deck_j2 = Deck(deck_j2_definitions, chargeur)

deck_j1.melanger()
deck_j2.melanger()

j1 = Joueur(nom="Alice", deck=deck_j1, pi=PI_DEPART, equipe=1)
j2 = Joueur(nom="Bob", deck=deck_j2, pi=PI_DEPART, equipe=2)

# Piocher les cartes initiales pour chaque joueur
for _ in range(TAILLE_MAIN_MAX):
    j1.get_main().ajouter_carte(j1.get_deck().piocher())
    j2.get_main().ajouter_carte(j2.get_deck().piocher())

demo = Classique([j1, j2], terrain_demo)

if __name__ == '__main__':

    vue = VueJeu(demo)
    vue.lancer()

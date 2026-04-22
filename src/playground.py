""" Fichier à lancer pour voir toutes les créatures, bâtiments et cases du jeu.
Les sorts seront en mains. """

from src.terrain import Terrain
from src.deck import Deck
from src.joueur import Joueur
from src.jeu import Classique
from src.chargeur.entite_chargeur import EntiteChargeur

def creer_playground()-> Classique:
    PI_DEPART = 100
    EXEMPLAIRE = 4
    TAILLE_MAIN_MAX = 6

    # Charger les entites
    chargeur = EntiteChargeur()
    chargeur.charger_toutes_les_entites()

    # Terrain avec les cases
    posNeutre = [(1, 0), (-1, 1), (-1, 0), (1, -1)]


    posj1 = [(-2, 0), (-2, 1), (-2, 2), (-3, 1), (-3, 2)]
    posj2 = [(-x, -y) for (x, y) in posj1]
    posj3 = [(-1, -1), (1, -2), (0, -2), (1, -3), (-1, -2)]
    posj4 = [(1, 1), (-1, +2), (-1, +3), (+1, +2)]

    # Case
    c_neutre = [chargeur.creer_instance("terrain", x, 0) for x in posNeutre]
    c_foret = [chargeur.creer_instance("foret", (0, 0), 0)]
    c_piques = [chargeur.creer_instance("piques", (0, -1), 0)]
    c_plaine = [chargeur.creer_instance("plaine", (0, 1), 0)]
    c_carriere = [chargeur.creer_instance("carriere", (0, 2), 4)]

    c_case = c_neutre + c_foret + c_piques + c_plaine + c_carriere

    # Créature
    c_chevalier = [chargeur.creer_instance("chevalier", (1, 0), 1)]
    c_fermier = [chargeur.creer_instance("fermier", (1, -1), 1)]
    c_bucheron = [chargeur.creer_instance("bucheron", (1, -2), 1)]
    c_archere = [chargeur.creer_instance("archere", (1, 1), 4)]
    c_belier = [chargeur.creer_instance("belier", (1, 2), 3)]

    c_temp = [chargeur.creer_instance("cercle", (1, 3), 1)]

    c_creature = c_chevalier + c_fermier + c_bucheron + c_archere + c_belier + c_temp

    # Batiment
    c_palissade = [chargeur.creer_instance("palissade", (-1, 0), 2)]
    c_feu_de_camp = [chargeur.creer_instance("feu de camp", (-1, 1), 2)]
    c_etendard = [chargeur.creer_instance("etendard", (-1, -1), 3)]

    c_batiment = c_palissade + c_feu_de_camp + c_etendard

    cj1 = [chargeur.creer_instance(
        "terrain", x, 1) for x in posj1]
    cj2 = [chargeur.creer_instance(
        "terrain", (x[0], x[1]), 2) for x in posj2]
    cj3 = [chargeur.creer_instance(
        "terrain", (x[0], x[1]), 3) for x in posj3]
    cj4 = [chargeur.creer_instance(
        "terrain", (x[0], x[1]), 4) for x in posj4]

    cj = cj1 + cj2 + cj3 + cj4

    terrain = cj + c_case + c_creature + c_batiment
    terrain_playground = Terrain(terrain)

    deck = []

    deck.append(Deck([("palissade", 2)] * EXEMPLAIRE + [("feu de camp", 2)] * EXEMPLAIRE + [("etendard", 3)] * EXEMPLAIRE, chargeur))

    deck.append(Deck([("chevalier", 1)] * EXEMPLAIRE + [("fermier", 1)] * EXEMPLAIRE + [("bucheron", 1)] * EXEMPLAIRE + [("archere", 1)] * EXEMPLAIRE + [("belier", 1)] * EXEMPLAIRE, chargeur))
    deck[1].melanger()

    deck.append(Deck([("foret", 3)] * EXEMPLAIRE + [("carriere", 3)] * EXEMPLAIRE + [("piques", 3)] * EXEMPLAIRE + [("plaine", 3)] * EXEMPLAIRE + [("terrain", 3)] * EXEMPLAIRE, chargeur))
    deck[2].melanger()

    deck.append(Deck([("archere", 4)] * EXEMPLAIRE + [("pluie de fleches", 4)] * EXEMPLAIRE + [("pluie", 4)] * EXEMPLAIRE, chargeur))
    deck[3].melanger()

    j1 = Joueur(nom="Alice", deck=deck[0], pi=PI_DEPART, equipe=1)
    j2 = Joueur(nom="Bob", deck=deck[1], pi=PI_DEPART, equipe=2)
    j3 = Joueur(nom="Charles", deck=deck[2], pi=PI_DEPART, equipe=3)
    j4 = Joueur(nom="Debby", deck=deck[3], pi=PI_DEPART, equipe=4)

    # Piocher les cartes initiales pour chaque joueur
    for _ in range(TAILLE_MAIN_MAX):
        j1.get_main().ajouter_carte(j1.get_deck().piocher())
        j2.get_main().ajouter_carte(j2.get_deck().piocher())
        j3.get_main().ajouter_carte(j3.get_deck().piocher())
        j4.get_main().ajouter_carte(j4.get_deck().piocher())

    return Classique([j1, j2, j3, j4], terrain_playground, mode_de_jeu="Classique", niveau="Playground")

if __name__ == '__main__':
    from src.app.application import Application
    app = Application("playground")
    app.lancer()

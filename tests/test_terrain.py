""" Fichier de test pour la classe Terrain """


# pylint: disable=missing-function-docstring, missing-class-docstring, C0200

import unittest
from random import randint
from tests.utils import MIN_INT, MAX_INT, BOUCLE_TEST
from src.case import Case
from src.creature import Creature
from src.batiment import Batiment
from src.effets import Effet
from src.sort import Sort
from src.terrain import Terrain


class TestTerrain(unittest.TestCase):

    def test__init__(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_get_entites(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_debut_tour(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_fin_tour(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_nettoyer_entites_mortes(self):
        cr1 = Creature(pv=0, nom="creature1", pos=(0, 0), cout=0, equipe=1, portee=0,
                      control=0, comp=[], combat=0, demolition=0, degradation=0, mouv=0)
        cr2 = Creature(pv=10, nom="creature2", pos=(0, 0), cout=0, equipe=1, portee=0,
                      control=0, comp=[], combat=0, demolition=0, degradation=0, mouv=0)
        bt1 = Batiment(pv=0, nom="batiment1", pos=(0, 0), cout=0, equipe=1, portee=0,
                      control=0, comp=[], combat=0, demolition=0, degradation=0,)
        bt2 = Batiment(pv=10, nom="batiment2", pos=(0, 0), cout=0, equipe=1, portee=0,
                      control=0, comp=[], combat=0, demolition=0, degradation=0,)
        case = Case(pv=0, nom="case", pos=(0, 0), cout=0, equipe=1,
                    control=0, control_max=10, comp=[])
        case2 = Case(pv=10, nom="case2", pos=(0, 0), cout=0, equipe=1,
                    control=0, control_max=10, comp=[])
        terrain = Terrain(entites=[cr1, cr2, bt1, bt2, case, case2])
        terrain.nettoyer_entites_mortes()
        self.assertNotIn(cr1, terrain.entites, "Creature morte non supprimée")
        self.assertIn(cr2, terrain.entites, "Creature vivante supprimée")
        self.assertNotIn(bt1, terrain.entites, "Batiment mort non supprimé")
        self.assertIn(bt2, terrain.entites, "Batiment vivant supprimé")
        self.assertNotIn(case, terrain.entites, "Case morte non supprimée")
        self.assertIn(case2, terrain.entites, "Case vivante supprimée")

    def test_get_case_at(self):
        for _ in range(BOUCLE_TEST):
            x = randint(MIN_INT, MAX_INT)
            y = randint(MIN_INT, MAX_INT)
            case = Case(pv=0, nom="", pos=(x, y), cout=0, equipe=0,
                        control=0, control_max=0, comp=[])
            cases = [Case(pv=0, nom="", pos=(randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT)),
                          cout=0, equipe=0, control=0, control_max=0, comp=[]) for _ in range(10)]
            terrain = Terrain(entites=cases + [case])
            self.assertEqual(terrain.get_case_at((x, y)), case)
            terrain = Terrain(entites=[case])
            self.assertEqual(terrain.get_case_at((x, y)), case)

            terrain2 = Terrain(entites=cases)
            self.assertIsNone(terrain2.get_case_at((x, y)), "get_case_at a trouvé une case inexistante")

    def test_avant_attaque(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_apres_attaque(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_effectuer_attaque(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_fin_tour_decremente_et_expire_mouille(self):
        case = Case(pv=10, nom="plaine", pos=(0, 0), cout=0, equipe=1,
                    control=0, control_max=10, comp=[])
        creature = Creature(pv=10, nom="creature", pos=(0, 0), cout=0, equipe=1, portee=0,
                            control=0, comp=[], combat=0, demolition=0, degradation=0, mouv=2)
        creature.ajouter_statut(Effet._creer_statut_depuis_id("mouille"))

        terrain = Terrain(entites=[case, creature])

        terrain.fin_tour(1)
        self.assertEqual(creature.get_statut("Mouille").get_duree_restante(), 2)
        self.assertEqual(creature.get_mouv_max(), 1)

        terrain.fin_tour(1)
        self.assertEqual(creature.get_statut("Mouille").get_duree_restante(), 1)

        terrain.fin_tour(1)
        self.assertIsNone(creature.get_statut("Mouille"))
        self.assertEqual(creature.get_mouv_max(), 2)
        self.assertEqual(creature.get_mouv(), 2)

    def test_effet_pluie_applique_mouille_sur_zone(self):
        case_centre = Case(pv=10, nom="centre", pos=(0, 0), cout=0, equipe=1,
                           control=0, control_max=10, comp=[])
        case_adjacente = Case(pv=10, nom="adj", pos=(1, 0), cout=0, equipe=1,
                              control=0, control_max=10, comp=[])
        case_exterieure = Case(pv=10, nom="loin", pos=(2, 0), cout=0, equipe=1,
                               control=0, control_max=10, comp=[])
        creature_centre = Creature(pv=10, nom="centre", pos=(0, 0), cout=0, equipe=1, portee=0,
                                   control=0, comp=[], combat=0, demolition=0, degradation=0, mouv=2)
        creature_adjacente = Creature(pv=10, nom="adj", pos=(1, 0), cout=0, equipe=1, portee=0,
                                      control=0, comp=[], combat=0, demolition=0, degradation=0, mouv=2)
        creature_exterieure = Creature(pv=10, nom="loin", pos=(2, 0), cout=0, equipe=1, portee=0,
                                       control=0, comp=[], combat=0, demolition=0, degradation=0, mouv=2)
        sort = Sort(nom="Pluie", pos=(0, 0), cout=1, equipe=1, comp=[])

        entites = [
            case_centre,
            case_adjacente,
            case_exterieure,
            creature_centre,
            creature_adjacente,
            creature_exterieure
        ]

        Effet.pluie(sort, entites, case_centre)

        self.assertIsNotNone(creature_centre.get_statut("Mouille"))
        self.assertIsNotNone(creature_adjacente.get_statut("Mouille"))
        self.assertIsNone(creature_exterieure.get_statut("Mouille"))
        self.assertEqual(creature_centre.get_statut("Mouille").get_duree_restante(), 3)

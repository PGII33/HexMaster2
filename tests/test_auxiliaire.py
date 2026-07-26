""" Fichier de test pour les fonctions auxiliaires du jeu """

# pylint: disable=missing-function-docstring, missing-class-docstring, C0200

import unittest
from random import randint
from tests.utils import BOUCLE_TEST, MAX_INT, MIN_INT
import src.auxiliaire as aux
from src.case import Case
from src.creature import Creature
from src.batiment import Batiment
from src.terrain import Terrain


class TestAuxiliaire(unittest.TestCase):

    def test_distance_hex(self):
        # Tests de propriétés avec des valeurs aléatoires
        for _ in range(BOUCLE_TEST):
            a = (randint(int(MIN_INT/2), int(MAX_INT/2)), randint(int(MIN_INT/2), int(MAX_INT/2)))
            b = (randint(int(MIN_INT/2), int(MAX_INT/2)), randint(int(MIN_INT/2), int(MAX_INT/2)))
            d = aux.distance_hex(a, b)

            # Propriété de symétrie
            self.assertEqual(d, aux.distance_hex(a=b, b=a),
                             f"La distance doit être symétrique : dist({a}, {b}) = {d} " +
                             f"mais dist({b}, {a}) = {aux.distance_hex(a=b, b=a)}")

            # Distance à soi-même est 0
            self.assertEqual(0, aux.distance_hex(a, a),
                             "La distance d'un point à lui-même doit être 0, " +
                             f"mais dist({a}, {a}) = {aux.distance_hex(a, a)}")

            # Distance toujours positive
            self.assertGreaterEqual(d, 0,
                                    "La distance ne peut être négative, " +
                                    f"mais dist({a}, {b}) = {d}")

        # Tests semi-exhaustifs avec des cas connus
        cas_test = [
            ((0, 0), (0, 0), 0),
            ((0, 0), (1, 0), 1),
            ((0, 0), (0, 1), 1),
            ((0, 0), (-1, 0), 1),
            ((0, 0), (0, -1), 1),
            ((0, 0), (1, 1), 2),
            ((0, 0), (2, 0), 2),
            ((0, 0), (0, 2), 2),
            ((0, 0), (3, -2), 3),
            ((0, 0), (-3, 2), 3),
            ((1, 1), (2, 2), 2),
            ((1, 1), (3, 3), 4),
            ((5, 3), (2, 5), 3),
        ]

        for a, b, dist_attendue in cas_test:
            dist_calculee = aux.distance_hex(a, b)
            self.assertEqual(dist_calculee, dist_attendue,
                             f"La distance entre {a} et {b} devrait être {dist_attendue}, " +
                             f"mais on obtient {dist_calculee}")

    def test_est_a_distance_hex(self):
        # Tests semi-exhaustifs
        cas_test = [
            ((0, 0), (0, 0), 0, True),
            ((0, 0), (1, 0), 1, True),
            ((0, 0), (1, 0), 2, False),
            ((0, 0), (2, 1), 3, True),
            ((0, 0), (2, 1), 2, False),
            ((0, 0), (3, -2), 3, True),
            ((1, 1), (2, 2), 2, True),
            ((1, 1), (2, 2), 1, False),
        ]

        for a, b, dist, resultat_attendu in cas_test:
            resultat = aux.est_a_distance_hex(a, b, dist)
            self.assertEqual(resultat, resultat_attendu,
                             f"est_a_distance_hex({a}, {b}, {dist}) devrait retourner " +
                             f"{resultat_attendu}, mais retourne {resultat}")

        # Tests aléatoires
        for _ in range(BOUCLE_TEST):
            a = (randint(-20, 20), randint(-20, 20))
            b = (randint(-20, 20), randint(-20, 20))
            dist_reelle = aux.distance_hex(a, b)

            # La distance réelle doit retourner True
            self.assertTrue(aux.est_a_distance_hex(a, b, dist_reelle),
                            f"Les points {a} et {b} sont à distance {dist_reelle}, " +
                            "mais est_a_distance_hex retourne False")

            # Toutes autres distances doivent retourner False
            for d in range(0, 10):
                if d != dist_reelle:
                    self.assertFalse(aux.est_a_distance_hex(a, b, d),
                                     f"Les points {a} et {b} ne sont pas à distance {d} " +
                                     f"(distance réelle = {dist_reelle}), " +
                                     "mais est_a_distance_hex retourne True")

    def test_est_a_portee_hex(self):
        # Tests semi-exhaustifs
        cas_test = [
            ((0, 0), (0, 0), 0, True),
            ((0, 0), (1, 0), 1, True),
            ((0, 0), (1, 0), 0, False),
            ((0, 0), (2, 1), 3, True),
            ((0, 0), (2, 1), 2, False),
            ((0, 0), (3, -2), 3, True),
            ((0, 0), (3, -2), 2, False),
            ((1, 1), (2, 2), 2, True),
            ((1, 1), (2, 2), 3, True),
            ((1, 1), (2, 2), 1, False),
        ]

        for a, b, portee, resultat_attendu in cas_test:
            resultat = aux.est_a_portee_hex(a, b, portee)
            self.assertEqual(resultat, resultat_attendu,
                             f"est_a_portee_hex({a}, {b}, {portee}) devrait retourner " +
                             f"{resultat_attendu}, mais retourne {resultat}")

        # Tests aléatoires
        for _ in range(BOUCLE_TEST):
            a = (randint(-20, 20), randint(-20, 20))
            b = (randint(-20, 20), randint(-20, 20))
            dist_reelle = aux.distance_hex(a, b)

            # Toutes portées >= distance réelle doivent retourner True
            for portee in range(dist_reelle, dist_reelle + 5):
                self.assertTrue(aux.est_a_portee_hex(a, b, portee),
                                f"Les points {a} et {b} sont à distance {dist_reelle}, " +
                                f"donc est_a_portee_hex avec portée {portee} devrait retourner True")

            # Toutes portées < distance réelle doivent retourner False
            for portee in range(0, max(0, dist_reelle)):
                self.assertFalse(aux.est_a_portee_hex(a, b, portee),
                                 f"Les points {a} et {b} sont à distance {dist_reelle}, " +
                                 f"donc est_a_portee_hex avec portée {portee} devrait retourner False")

    def test_a_distance_hex(self):
        # Test distance 0 : seulement le point lui-même
        centre = (0, 0)
        points_dist_0 = aux.a_distance_hex(centre, 0)
        self.assertEqual(len(points_dist_0), 1,
                         "À distance 0, il devrait y avoir exactement 1 point, " +
                         f"mais on en trouve {len(points_dist_0)}")
        self.assertIn(centre, points_dist_0,
                      f"À distance 0 de {centre}, le seul point devrait être {centre}")

        # Test distance 1 : 6 adjacents
        points_dist_1 = aux.a_distance_hex(centre, 1)
        adjacents_attendus = [(1, 0), (0, 1), (-1, 1),
                              (-1, 0), (0, -1), (1, -1)]
        self.assertEqual(len(points_dist_1), 6,
                         "À distance 1, il devrait y avoir 6 points, " +
                         f"mais on en trouve {len(points_dist_1)}")
        for adj in adjacents_attendus:
            self.assertIn(adj, points_dist_1,
                          f"Le point {adj} devrait être à distance 1 de {centre}")

        # Test distance 2 : 12 points
        points_dist_2 = aux.a_distance_hex(centre, 2)
        self.assertEqual(len(points_dist_2), 12,
                         "À distance 2, il devrait y avoir 12 points, " +
                         f"mais on en trouve {len(points_dist_2)}")

        # Vérifier que chaque point retourné est bien à la distance demandée
        for d in range(0, 5):
            points = aux.a_distance_hex(centre, d)
            for point in points:
                dist_calculee = aux.distance_hex(centre, point)
                self.assertEqual(dist_calculee, d,
                                 f"Le point {point} retourné par a_distance_hex({centre}, {d}) " +
                                 f"est à distance {dist_calculee}, pas {d}")

        # Test avec un centre différent
        centre2 = (3, -2)
        for d in range(0, 4):
            points = aux.a_distance_hex(centre2, d)
            for point in points:
                dist_calculee = aux.distance_hex(centre2, point)
                self.assertEqual(dist_calculee, d,
                                 f"Le point {point} retourné par a_distance_hex({centre2}, {d}) " +
                                 f"est à distance {dist_calculee}, pas {d}")

        # Vérification du nombre de points par distance (formule : 6*d pour d>0, 1 pour d=0)
        for d in range(1, 5):
            points = aux.a_distance_hex((0, 0), d)
            self.assertEqual(len(points), 6 * d,
                             f"À distance {d}, il devrait y avoir {6*d} points, " +
                             f"mais on en trouve {len(points)}")

    def test_a_portee_hex(self):
        # Test portée 0 : seulement le point lui-même
        centre = (0, 0)
        points_portee_0 = aux.a_portee_hex(centre, 0)
        self.assertEqual(len(points_portee_0), 1,
                         "À portée 0, il devrait y avoir exactement 1 point, " +
                         f"mais on en trouve {len(points_portee_0)}")
        self.assertIn(centre, points_portee_0,
                      f"À portée 0 de {centre}, le seul point devrait être {centre}")

        # Test portée 1 : 1 + 6 = 7 points
        points_portee_1 = aux.a_portee_hex(centre, 1)
        self.assertEqual(len(points_portee_1), 7,
                         "À portée 1, il devrait y avoir 7 points, " +
                         f"mais on en trouve {len(points_portee_1)}")

        # Test portée 2 : 1 + 6 + 12 = 19 points
        points_portee_2 = aux.a_portee_hex(centre, 2)
        self.assertEqual(len(points_portee_2), 19,
                         "À portée 2, il devrait y avoir 19 points, " +
                         f"mais on en trouve {len(points_portee_2)}")

        # Vérifier que chaque point retourné est bien à portée
        for portee in range(0, 5):
            points = aux.a_portee_hex(centre, portee)
            for point in points:
                dist_calculee = aux.distance_hex(centre, point)
                self.assertLessEqual(dist_calculee, portee,
                                     f"Le point {point} retourné par a_portee_hex({centre}, {portee}) " +
                                     f"est à distance {dist_calculee}, ce qui dépasse la portée {portee}")

        # Vérifier que tous les points à portée sont bien présents
        for portee in range(0, 4):
            points_a_portee = aux.a_portee_hex(centre, portee)
            for d in range(portee + 1):
                points_a_distance_d = aux.a_distance_hex(centre, d)
                for point in points_a_distance_d:
                    self.assertIn(point, points_a_portee,
                                  f"Le point {point} à distance {d} devrait être dans " +
                                  f"a_portee_hex({centre}, {portee})")

        # Test avec un centre différent
        centre2 = (5, -3)
        for portee in range(0, 4):
            points = aux.a_portee_hex(centre2, portee)
            for point in points:
                dist_calculee = aux.distance_hex(centre2, point)
                self.assertLessEqual(dist_calculee, portee,
                                     f"Le point {point} à distance {dist_calculee} ne devrait pas " +
                                     f"être dans a_portee_hex({centre2}, {portee})")

        # Vérification du nombre de points par portée (formule : 1 + 3*p*(p+1) pour p>=0)
        for portee in range(0, 5):
            points = aux.a_portee_hex((0, 0), portee)
            nb_attendu = 1 + 3 * portee * (portee + 1)
            self.assertEqual(len(points), nb_attendu,
                             f"À portée {portee}, il devrait y avoir {nb_attendu} points, " +
                             f"mais on en trouve {len(points)}")

    def test_adjacents_hex(self):
        # Test pour le centre (0, 0)
        centre = (0, 0)
        adjacents = aux.adjacents_hex(centre)
        adjacents_attendus = [(1, 0), (0, 1), (-1, 1),
                              (-1, 0), (0, -1), (1, -1)]

        self.assertEqual(len(adjacents), 6,
                         "Un hexagone devrait avoir 6 adjacents, " +
                         f"mais adjacents_hex({centre}) en retourne {len(adjacents)}")

        for adj in adjacents_attendus:
            self.assertIn(adj, adjacents,
                          f"Le point {adj} devrait être adjacent à {centre}, " +
                          "mais n'est pas dans la liste retournée")

        # Vérifier que tous les adjacents sont à distance 1
        for adj in adjacents:
            dist = aux.distance_hex(centre, adj)
            self.assertEqual(dist, 1,
                             "Un point adjacent devrait être à distance 1, " +
                             f"mais {adj} est à distance {dist} de {centre}")

        # Test avec différents centres
        centres_test = [(1, 1), (5, 3), (-2, 4), (10, -5)]
        for centre_test in centres_test:
            adjacents_test = aux.adjacents_hex(centre_test)

            self.assertEqual(len(adjacents_test), 6,
                             "Un hexagone devrait avoir 6 adjacents, " +
                             f"mais adjacents_hex({centre_test}) en retourne {len(adjacents_test)}")

            for adj in adjacents_test:
                dist = aux.distance_hex(centre_test, adj)
                self.assertEqual(dist, 1,
                                 "Un point adjacent devrait être à distance 1, " +
                                 f"mais {adj} est à distance {dist} de {centre_test}")

            # Vérifier que les adjacents sont équivalents à a_distance_hex(..., 1)
            adjacents_via_distance = aux.a_distance_hex(centre_test, 1)
            self.assertEqual(set(adjacents_test), set(adjacents_via_distance),
                             f"adjacents_hex({centre_test}) devrait retourner les mêmes points " +
                             f"que a_distance_hex({centre_test}, 1)")

    def test_get_cases_deplacement(self):
        # Création d'un terrain simple avec des cases
        cases = [
            Case(pv=10, nom="Case1", pos=(0, 0), cout=0,
                 equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Case2", pos=(1, 0), cout=0,
                 equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Case3", pos=(0, 1), cout=0,
                 equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Case4", pos=(1, 1), cout=0,
                 equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Case5", pos=(2, 0), cout=0,
                 equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Case6", pos=(0, 2), cout=0,
                 equipe=0, control=0, control_max=10, comp=[]),
        ]

        # Test 1 : Créature avec mouvement 1, aucun obstacle
        creature1 = Creature(pv=10, nom="Creature1", pos=(0, 0), cout=1, equipe=1,
                             combat=1, demolition=0, degradation=0, portee=1,
                             control=1, mouv=1)
        terrain1 = Terrain(entites=cases + [creature1])

        cases_deplacement1 = aux.get_cases_deplacement(creature1, terrain1)
        # La case actuelle (0, 0) est aussi incluse car c'est une entité séparée de la créature
        positions_attendues1 = [(0, 0), (1, 0), (0, 1)]

        self.assertEqual(len(cases_deplacement1), len(positions_attendues1),
                         f"Avec mouvement 1, il devrait y avoir {len(positions_attendues1)} cases " +
                         f"de déplacement, mais on en trouve {len(cases_deplacement1)}")

        for pos in positions_attendues1:
            self.assertIn(pos, cases_deplacement1,
                          f"La position {pos} devrait être accessible avec mouvement 1 depuis (0, 0)")

        # Test 2 : Créature avec mouvement 2
        creature2 = Creature(pv=10, nom="Creature2", pos=(0, 0), cout=1, equipe=1,
                             combat=1, demolition=0, degradation=0, portee=1,
                             control=1, mouv=2)
        terrain2 = Terrain(entites=cases + [creature2])

        cases_deplacement2 = aux.get_cases_deplacement(creature2, terrain2)
        # Inclut la case actuelle (0, 0) plus les cases accessibles
        positions_attendues2 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]

        for pos in positions_attendues2:
            self.assertIn(pos, cases_deplacement2,
                          f"La position {pos} devrait être accessible avec mouvement 2 depuis (0, 0)")

        # Test 3 : Case occupée par une autre créature
        creature3_principale = Creature(pv=10, nom="Creature3", pos=(0, 0), cout=1, equipe=1,
                                        combat=1, demolition=0, degradation=0, portee=1,
                                        control=1, mouv=1)
        creature3_obstacle = Creature(pv=10, nom="Obstacle", pos=(1, 0), cout=1, equipe=2,
                                      combat=1, demolition=0, degradation=0, portee=1,
                                      control=1, mouv=1)
        terrain3 = Terrain(
            entites=cases + [creature3_principale, creature3_obstacle])

        cases_deplacement3 = aux.get_cases_deplacement(
            creature3_principale, terrain3)

        self.assertNotIn((1, 0), cases_deplacement3,
                         "La position (1, 0) est occupée par une autre créature, " +
                         "elle ne devrait pas être accessible")
        self.assertIn((0, 1), cases_deplacement3,
                      "La position (0, 1) est libre, elle devrait être accessible")

        # Test 4 : Case occupée par un bâtiment
        creature4 = Creature(pv=10, nom="Creature4", pos=(0, 0), cout=1, equipe=1,
                             combat=1, demolition=0, degradation=0, portee=1,
                             control=1, mouv=1)
        batiment = Batiment(pv=20, nom="Batiment", pos=(1, 0), cout=2, equipe=1,
                            combat=0, demolition=0, degradation=0, portee=0,
                            control=2, comp=[])
        terrain4 = Terrain(entites=cases + [creature4, batiment])

        cases_deplacement4 = aux.get_cases_deplacement(creature4, terrain4)

        self.assertNotIn((1, 0), cases_deplacement4,
                         "La position (1, 0) est occupée par un bâtiment, " +
                         "elle ne devrait pas être accessible")

        # Test 5 : Mouvement 0 - la créature peut rester sur sa case actuelle
        creature5 = Creature(pv=10, nom="Creature5", pos=(0, 0), cout=1, equipe=1,
                             combat=1, demolition=0, degradation=0, portee=1,
                             control=1, mouv=0)
        terrain5 = Terrain(entites=cases + [creature5])

        cases_deplacement5 = aux.get_cases_deplacement(creature5, terrain5)

        self.assertEqual(len(cases_deplacement5), 1,
                         "Avec mouvement 0, il devrait y avoir seulement la case actuelle, " +
                         f"mais on en trouve {len(cases_deplacement5)}")
        self.assertIn((0, 0), cases_deplacement5,
                      "Avec mouvement 0, la créature devrait au moins pouvoir rester sur sa case actuelle")

    def test_get_entites_a_portee(self):
        # Création d'un terrain avec plusieurs entités
        cases = [
            Case(pv=10, nom="Case", pos=(i, j), cout=0,
                 equipe=0, control=0, control_max=10, comp=[])
            for i in range(-3, 4) for j in range(-3, 4)
        ]

        # Test 1 : Portée 1
        creature_attaquante1 = Creature(pv=10, nom="Attaquant", pos=(0, 0), cout=1, equipe=1,
                                        combat=5, demolition=0, degradation=0, portee=1,
                                        control=1, mouv=1)
        cible1 = Creature(pv=10, nom="Cible1", pos=(1, 0), cout=1, equipe=2,
                          combat=1, demolition=0, degradation=0, portee=1,
                          control=1, mouv=1)
        cible2 = Creature(pv=10, nom="Cible2", pos=(0, 1), cout=1, equipe=2,
                          combat=1, demolition=0, degradation=0, portee=1,
                          control=1, mouv=1)
        hors_portee = Creature(pv=10, nom="HorsPortee", pos=(2, 0), cout=1, equipe=2,
                               combat=1, demolition=0, degradation=0, portee=1,
                               control=1, mouv=1)

        terrain1 = Terrain(
            entites=cases + [creature_attaquante1, cible1, cible2, hors_portee])
        entites_a_portee1 = aux.get_entites_a_portee(
            creature_attaquante1, terrain1)

        self.assertIn(cible1, entites_a_portee1,
                      f"La créature {cible1.nom} à position {cible1.get_pos()} devrait être à portée 1")
        self.assertIn(cible2, entites_a_portee1,
                      f"La créature {cible2.nom} à position {cible2.get_pos()} devrait être à portée 1")
        self.assertNotIn(hors_portee, entites_a_portee1,
                         f"La créature {hors_portee.nom} à position {hors_portee.get_pos()} " +
                         "ne devrait pas être à portée 1")
        self.assertNotIn(creature_attaquante1, entites_a_portee1,
                         "La créature attaquante ne devrait pas être dans sa propre liste de cibles")

        # Test 2 : Portée 2
        creature_attaquante2 = Creature(pv=10, nom="Attaquant2", pos=(0, 0), cout=1, equipe=1,
                                        combat=5, demolition=0, degradation=0, portee=2,
                                        control=1, mouv=1)
        terrain2 = Terrain(
            entites=cases + [creature_attaquante2, cible1, cible2, hors_portee])
        entites_a_portee2 = aux.get_entites_a_portee(
            creature_attaquante2, terrain2)

        self.assertIn(cible1, entites_a_portee2,
                      "La créature à distance 1 devrait être à portée 2")
        self.assertIn(hors_portee, entites_a_portee2,
                      "La créature à distance 2 devrait être à portée 2")

        # Test 3 : Portée 0 (seulement sa propre case)
        creature_attaquante3 = Creature(pv=10, nom="Attaquant3", pos=(0, 0), cout=1, equipe=1,
                                        combat=5, demolition=0, degradation=0, portee=0,
                                        control=1, mouv=1)
        case_meme_position = Case(pv=10, nom="CaseMeme", pos=(0, 0), cout=0, equipe=0,
                                  control=0, control_max=10, comp=[])
        terrain3 = Terrain(
            entites=cases + [creature_attaquante3, case_meme_position, cible1])
        entites_a_portee3 = aux.get_entites_a_portee(
            creature_attaquante3, terrain3)

        self.assertIn(case_meme_position, entites_a_portee3,
                      "Avec portée 0, la case à la même position devrait être à portée")
        self.assertNotIn(cible1, entites_a_portee3,
                         "Avec portée 0, une créature adjacente ne devrait pas être à portée")
        self.assertNotIn(creature_attaquante3, entites_a_portee3,
                         "La créature attaquante ne devrait pas être dans sa propre liste de cibles")

        # Test 4 : Bâtiment avec portée
        batiment_attaquant = Batiment(pv=20, nom="Tour", pos=(0, 0), cout=3, equipe=1,
                                      combat=3, demolition=0, degradation=0, portee=2,
                                      control=2, comp=[])
        terrain4 = Terrain(
            entites=cases + [batiment_attaquant, cible1, cible2, hors_portee])
        entites_a_portee4 = aux.get_entites_a_portee(
            batiment_attaquant, terrain4)

        self.assertIn(cible1, entites_a_portee4,
                      "Le bâtiment avec portée 2 devrait pouvoir atteindre une créature à distance 1")
        self.assertIn(hors_portee, entites_a_portee4,
                      "Le bâtiment avec portée 2 devrait pouvoir atteindre une créature à distance 2")

        # Test 5 : Vérifier que toutes les cases sont incluses
        creature_attaquante5 = Creature(pv=10, nom="Attaquant5", pos=(0, 0), cout=1, equipe=1,
                                        combat=5, demolition=0, degradation=0, portee=2,
                                        control=1, mouv=1)
        terrain5 = Terrain(entites=cases + [creature_attaquante5])
        entites_a_portee5 = aux.get_entites_a_portee(
            creature_attaquante5, terrain5)

        # Vérifier que les cases dans la portée sont bien présentes
        nb_cases_attendues = sum(1 for c in cases
                                 if aux.est_a_portee_hex(creature_attaquante5.get_pos(), c.get_pos(), 2))
        self.assertEqual(len(entites_a_portee5), nb_cases_attendues,
                         f"Avec portée 2, il devrait y avoir {nb_cases_attendues} cases à portée, " +
                         f"mais on en trouve {len(entites_a_portee5)}")

    def test_get_cases_deplacement_ne_traverse_pas_les_obstacles(self):
        cases = [
            Case(pv=10, nom="Origine", pos=(0, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Bloquee", pos=(1, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="DerriereObstacle", pos=(2, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
        ]

        creature = Creature(pv=10, nom="Marcheur", pos=(0, 0), cout=1, equipe=1,
                        combat=1, demolition=0, degradation=0, portee=1,
                        control=1, mouv=3)
        obstacle = Creature(pv=10, nom="Obstacle", pos=(1, 0), cout=1, equipe=2,
                        combat=1, demolition=0, degradation=0, portee=1,
                        control=1, mouv=1)
        terrain = Terrain(entites=cases + [creature, obstacle])

        cases_deplacement = aux.get_cases_deplacement(creature, terrain)

        self.assertNotIn((1, 0), cases_deplacement,
                    "Une case occupée par une créature ne doit pas être traversable")
        self.assertNotIn((2, 0), cases_deplacement,
                    "Une case derrière un obstacle bloquant ne doit pas être atteignable")

    def test_get_cases_deplacement_ne_traverse_pas_le_vide(self):
        cases = [
            Case(pv=10, nom="Origine", pos=(0, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Isolee", pos=(2, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
        ]

        creature = Creature(pv=10, nom="Marcheur", pos=(0, 0), cout=1, equipe=1,
                        combat=1, demolition=0, degradation=0, portee=1,
                        control=1, mouv=3)
        terrain = Terrain(entites=cases + [creature])

        cases_deplacement = aux.get_cases_deplacement(creature, terrain)

        self.assertIn((0, 0), cases_deplacement,
                    "La case d'origine doit rester accessible")
        self.assertNotIn((2, 0), cases_deplacement,
                    "Une case séparée par du vide ne doit pas être atteignable")

    def test_get_cout_deplacement_prend_en_compte_le_chemin_reel(self):
        cases = [
            Case(pv=10, nom="Origine", pos=(0, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Bloquee", pos=(1, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Contournement1", pos=(0, 1), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Contournement2", pos=(1, 1), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
            Case(pv=10, nom="Destination", pos=(2, 0), cout=0,
                equipe=0, control=0, control_max=10, comp=[]),
        ]

        creature = Creature(pv=10, nom="Marcheur", pos=(0, 0), cout=1, equipe=1,
                        combat=1, demolition=0, degradation=0, portee=1,
                        control=1, mouv=4)
        obstacle = Batiment(pv=20, nom="Mur", pos=(1, 0), cout=1, equipe=2,
                        combat=0, demolition=0, degradation=0, portee=0,
                        control=1, comp=[])
        terrain = Terrain(entites=cases + [creature, obstacle])

        cout = aux.get_cout_deplacement(creature, terrain, (2, 0))

        self.assertEqual(cout, 3,
                    "Le coût doit suivre le chemin de contournement réel, pas la distance hex directe")

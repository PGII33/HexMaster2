""" Fichier de test pour les fonctions auxiliaires du jeu """

# pylint: disable=missing-function-docstring, missing-class-docstring, C0200

import unittest
from random import randint
from tests.utils import BOUCLE_TEST, MAX_INT, MIN_INT
import src.auxliaire as aux


class TestAuxiliaire(unittest.TestCase):

    def test_distance_hex(self):
        for _ in range(BOUCLE_TEST):
            a = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            b = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            d = aux.distance_hex(a, b)

            self.assertEqual(d, aux.distance_hex(a=b, b=a), "La distance " +
                             "(a, b) doit être la même que (b, a), et pourtant, " +
                             f"dist(a,b) = {d} et dist(b,a) = {aux.distance_hex(a=b, b=a)} " +
                             f"pour les points {a} et {b}")
            self.assertEqual(0, aux.distance_hex(a, a))
            self.assertTrue(
                d >= 0, f"La distance ne peut être négative, pourtant on a distance(a, b) = {d} les points {a} et {b}")

        # Test de semi-exhaustifs
        points = [(0, 0), (1, 0), (0, 1), (1, 1), (3, -2), (-3, 2)]
        dists = [0, 1, 1, 2, 3, 3]
        for k in range(len(points)):
            self.assertEqual(aux.distance_hex(points[0], points[k]), dists[k],
                             f"La distance entre {points[0]} et {points[k]} devrait être {dists[k]}")

    def test_est_a_distance_hex(self):
        # Tests semi-exhaustifs
        points = [(0, 0), (1, 0), (0, 1), (1, 1), (3, -2), (-3, 2)]
        dists = [0, 1, 1, 2, 3, 3]
        for k in range(len(points)):
            self.assertTrue(aux.est_a_distance_hex(points[0], points[k], dists[k]),
                            f"La distance entre {points[0]} et {points[k]} devrait être {dists[k]}")
            for _ in range(BOUCLE_TEST):
                d = randint(0, 10)
                while d == dists[k]:
                    d = randint(0, 10)
                self.assertFalse(aux.est_a_distance_hex(points[0], points[k], d),
                                 f"La distance entre {points[0]} et {points[k]} ne" +
                                 f"devrait pas être {d}, pourtant est_a_distance_hex" +
                                 f"({points[0]}, {points[k]}, {d}) = True")

    def test_est_a_portee_hex(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_a_distance_hex(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_a_portee_hex(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_adjacents_hex(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_get_cases_deplacement(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_get_entites_a_portee(self):
        """ Pas implémenté """  # TODO: Implémenter
        self.skipTest("Pas implémenté")

""" Fichier de tests de la classe Joueur """

# pylint: disable=missing-function-docstring, missing-class-docstring

import unittest
from random import randint
from src.joueur import Joueur
from tests.utils import generate_random_string, BOUCLE_TEST, TAILLE_STR, MAX_INT


class TestJoueur(unittest.TestCase):

    def test__init__(self):
        """ Pas Implementé """  # TODO: #19 implémenter ce test

    def test_get_nom(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            joueur = Joueur(nom, None, 0, 0)
            self.assertEqual(joueur.get_nom(), nom)

    def test_set_nom(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            joueur = Joueur("", None, 0, 0)
            joueur.set_nom(nom)
            self.assertEqual(joueur.get_nom(), nom)

    def test_get_deck(self):
        """ Pas Implementé """  # TODO: #20 implémenter ce test

    def test_get_main(self):
        """ Pas Implementé """  # TODO: #22 implémenter ce test

    def test_get_pi(self):
        for _ in range(BOUCLE_TEST):
            pi = randint(0, MAX_INT)
            joueur = Joueur("", None, pi, 0)
            self.assertEqual(joueur.get_pi(), pi)

    def test_set_pi(self):
        for _ in range(BOUCLE_TEST):
            pi = randint(0, MAX_INT)
            joueur = Joueur("", None, 0, 0)
            joueur.set_pi(pi)
            self.assertEqual(joueur.get_pi(), pi)

    def test_get_equipe(self):
        for _ in range(BOUCLE_TEST):
            equipe = randint(0, MAX_INT)
            joueur = Joueur("", None, 0, equipe)
            self.assertEqual(joueur.get_equipe(), equipe)

    def test_piocher_cartes(self):
        """ Pas Implementé """ # TODO: #21 implémenter ce test

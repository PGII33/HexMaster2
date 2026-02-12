""" Fichier de tests de la classe Unite """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.unite import Unite
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestUnite(unittest.TestCase):

    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            ctrl = randint(MIN_INT, MAX_INT)
            combat = randint(MIN_INT, MAX_INT)
            demolition = randint(MIN_INT, MAX_INT)
            degradation = randint(MIN_INT, MAX_INT)
            portee = randint(MIN_INT, MAX_INT)
            Unite(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe, control=ctrl,
                  combat=combat, demolition=demolition, degradation=degradation, portee=portee)

    def test_attaquer(self):
        """ Pas implémenté """ #TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_fin_tour(self):
        """ Pas implémenté """ #TODO: Implémenter
        self.skipTest("Pas implémenté")

    def test_get_a_attaque(self):
        for _ in range(BOUCLE_TEST):
            a_attaque = randint(0, 1)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_a_attaque(a_attaque)
            self.assertEqual(unite.get_a_attaque(), a_attaque)

    def test_set_a_attaque(self):
        for _ in range(BOUCLE_TEST):
            a_attaque = randint(0, 1)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_a_attaque(a_attaque)
            self.assertEqual(unite.get_a_attaque(), a_attaque)

    def test_get_combat(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=combat, demolition=0, degradation=0, portee=0)
            self.assertEqual(unite.get_combat(), combat)

    def test_set_combat(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_combat(combat)
            self.assertEqual(unite.get_combat(), combat)

    def test_get_demolition(self):
        for _ in range(BOUCLE_TEST):
            demolition = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=demolition, degradation=0, portee=0)
            self.assertEqual(unite.get_demolition(), demolition)

    def test_set_demolition(self):
        for _ in range(BOUCLE_TEST):
            demolition = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_demolition(demolition)
            self.assertEqual(unite.get_demolition(), demolition)

    def test_get_degradation(self):
        for _ in range(BOUCLE_TEST):
            degradation = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=degradation, portee=0)
            self.assertEqual(unite.get_degradation(), degradation)

    def test_set_degradation(self):
        for _ in range(BOUCLE_TEST):
            degradation = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_degradation(degradation)
            self.assertEqual(unite.get_degradation(), degradation)

    def test_get_portee(self):
        for _ in range(BOUCLE_TEST):
            portee = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=portee)
            self.assertEqual(unite.get_portee(), portee)

    def test_set_portee(self):
        for _ in range(BOUCLE_TEST):
            portee = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_portee(portee)
            self.assertEqual(unite.get_portee(), portee)

""" Fichier de tests de la classe Entite """

#pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.entite import Entite
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR

class TestEntite(unittest.TestCase):
    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            ctrl = randint(MIN_INT, MAX_INT)
            Entite(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                   control=ctrl, comp=[])

    def test_get_pv(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            entite = Entite(pv=pv, nom="", cout=0, pos=(0, 0), equipe=0,
                            control=0)
            self.assertEqual(entite.get_pv(), pv)

    def test_set_pv(self):
        for _ in range(BOUCLE_TEST):
            initial_pv = randint(MIN_INT, MAX_INT)
            new_pv = randint(MIN_INT, MAX_INT)
            entite = Entite(pv=initial_pv, nom="", cout=0, pos=(0, 0), equipe=0,
                            control=0)
            entite.set_pv(new_pv)
            self.assertEqual(entite.get_pv(), new_pv)

    def test_get_control(self):
        for _ in range(BOUCLE_TEST):
            control = randint(MIN_INT, MAX_INT)
            entite = Entite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                            control=control)
            self.assertEqual(entite.get_control(), control)

    def test_set_control(self):
        for _ in range(BOUCLE_TEST):
            initial_control = randint(MIN_INT, MAX_INT)
            new_control = randint(MIN_INT, MAX_INT)
            entite = Entite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                            control=initial_control)
            entite.set_control(new_control)
            self.assertEqual(entite.get_control(), new_control)

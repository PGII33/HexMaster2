""" Fichier de tests de la classe Case """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.case import Case
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestCase(unittest.TestCase):
    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            ctrl = randint(MIN_INT, MAX_INT)
            ctrl_max = randint(MIN_INT, MAX_INT)
            Case(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                 control=ctrl, control_max=ctrl_max, comp=[])

    def test_est_case(self):
        for _ in range(BOUCLE_TEST):
            case = Case(pv=0, nom="", pos=(0, 0), cout=0, equipe=0,
                        control=0, control_max=0, comp=[])
            self.assertTrue(case.est_case())

    def test_get_control_max(self):
        for _ in range(BOUCLE_TEST):
            ctrl_max = randint(MIN_INT, MAX_INT)
            case = Case(pv=0, nom="", pos=(0, 0), cout=0, equipe=0,
                        control=0, control_max=ctrl_max, comp=[])
            self.assertEqual(case.get_control_max(), ctrl_max)

    def test_set_control_max(self):
        for _ in range(BOUCLE_TEST):
            ctrl_max = randint(MIN_INT, MAX_INT)
            case = Case(pv=0, nom="", pos=(0, 0), cout=0, equipe=0,
                        control=0, control_max=0, comp=[])
            case.set_control_max(ctrl_max)
            self.assertEqual(case.get_control_max(), ctrl_max)

    def test_appliquer_control(self):
        """ Pas implémenté """ #TODO: Implémenter
        self.skipTest("Pas implémenté")

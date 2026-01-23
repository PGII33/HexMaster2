""" Fichier de tests de la classe Case """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.case import Case
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestEntite(unittest.TestCase):
    def test_init(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            co = randint(MIN_INT, MAX_INT)
            dm = randint(MIN_INT, MAX_INT)
            dg = randint(MIN_INT, MAX_INT)
            portee = randint(MIN_INT, MAX_INT)
            ctrl = randint(MIN_INT, MAX_INT)
            Case(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe, combat=co,
                 demolition=dm, degradation=dg, control=ctrl,
                 portee=portee, comp=[])

    def test_est_occupe(self):
        """ Non implémenté """
        self.skipTest("Pas implémenté")

    def test_est_case(self):
        for _ in range(BOUCLE_TEST):
            sort = Case(pv=0, nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, control=0,
                        portee=0, comp=[])
            self.assertTrue(sort.est_case())

if __name__ == '__main__':
    unittest.main()

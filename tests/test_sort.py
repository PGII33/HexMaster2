""" Fichier de tests de la classe Sort """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.sort import Sort
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestEntite(unittest.TestCase):
    def test_init(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            co = randint(MIN_INT, MAX_INT)
            dm = randint(MIN_INT, MAX_INT)
            dg = randint(MIN_INT, MAX_INT)
            portee = randint(MIN_INT, MAX_INT)
            Sort(nom=nom, pos=pos, cout=cout, equipe=equipe, combat=co,
                 demolition=dm, degradation=dg, portee=portee, comp=[])

    def test_est_sort(self):
        for _ in range(BOUCLE_TEST):
            sort = Sort(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            self.assertTrue(sort.est_sort())

if __name__ == '__main__':
    unittest.main()

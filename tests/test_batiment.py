""" Fichier de tests de la classe Batiment """

#pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.batiment import Batiment
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR

class TestBatiment(unittest.TestCase):
    def test__init__(self):
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
            Batiment(pv=pv, nom=nom, cout=cout, pos=pos, equipe=equipe,
                     combat=co, demolition=dm, degradation=dg, portee=portee,
                     control=ctrl)

    def test_est_batiment(self):
        for _ in range(BOUCLE_TEST):
            batiment = Batiment(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0)
            self.assertTrue(batiment.est_batiment())

if __name__ == '__main__':
    unittest.main()

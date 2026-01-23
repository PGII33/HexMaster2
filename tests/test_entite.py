""" Fichier de tests de la classe Entite """

#pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.entite import Entite
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
            Entite(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe,
                   combat=co, demolition=dm, degradation=dg, portee=portee,
                   control=ctrl, comp=[])

    def test_est_en_vie(self):
        """ Pas encore implémenté """
        self.skipTest("Test non implémenté")

    def test_get_pv(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            entite = Entite(pv=pv, nom="", cout=0, pos=(0, 0), equipe=0,
                            combat=0, demolition=0, degradation=0, portee=0, control=0)
            self.assertEqual(entite.get_pv(), pv)

    def test_set_en_vie(self):
        for _ in range(BOUCLE_TEST):
            valeur = bool(randint(0, 1))
            entite = Entite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                            combat=0, demolition=0, degradation=0, portee=0, control=0)
            entite.set_en_vie(valeur)
            self.assertEqual(entite.est_en_vie(), valeur)

    def test_set_pv(self):
        for _ in range(BOUCLE_TEST):
            initial_pv = randint(MIN_INT, MAX_INT)
            new_pv = randint(MIN_INT, MAX_INT)
            entite = Entite(pv=initial_pv, nom="", cout=0, pos=(0, 0), equipe=0,
                            combat=0, demolition=0, degradation=0, portee=0, control=0)
            entite.set_pv(new_pv)
            self.assertEqual(entite.get_pv(), new_pv)

if __name__ == '__main__':
    unittest.main()

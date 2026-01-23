""" Fichier de tests de la classe Creature """

#pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.creature import Creature
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR

class TestCreature(unittest.TestCase):
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
            mouv = randint(MIN_INT, MAX_INT)
            Creature(pv=pv, nom=nom, cout=cout, pos=pos, equipe=equipe,
                     combat=co, demolition=dm, degradation=dg, portee=portee,
                     control=ctrl, mouv=mouv)

    def test_get_mouv(self):
        for _ in range(BOUCLE_TEST):
            mouv = randint(MIN_INT, MAX_INT)
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=mouv)
            self.assertEqual(creature.get_mouv(), mouv)

    def test_set_mouv(self):
        for _ in range(BOUCLE_TEST):
            initial_mouv = randint(MIN_INT, MAX_INT)
            new_mouv = randint(MIN_INT, MAX_INT)
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=initial_mouv)
            creature.set_mouv(new_mouv)
            self.assertEqual(creature.get_mouv(), new_mouv)

    def test_est_creature(self):
        for _ in range(BOUCLE_TEST):
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=0)
            self.assertTrue(creature.est_creature())

if __name__ == '__main__':
    unittest.main()

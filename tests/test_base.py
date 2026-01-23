""" Fichier de tests de la classe Base """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.base import Base
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
            Base(nom=nom, pos=pos, cout=cout, equipe=equipe, combat=co,
                 demolition=dm, degradation=dg, portee=portee, comp=[])

    def test_get_nom(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            base = Base(nom=nom, pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            self.assertEqual(base.get_nom(), nom)

    def test_get_pos(self):
        for _ in range(BOUCLE_TEST):
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            base = Base(nom="", pos=pos, cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            self.assertEqual(base.get_pos(), pos)

    def test_get_cout(self):
        for _ in range(BOUCLE_TEST):
            cout = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=cout, equipe=0,
                        combat=0, demolition=0, degradation=0, portee=0, comp=[])
            self.assertEqual(base.get_cout(), cout)

    def test_get_portee(self):
        for _ in range(BOUCLE_TEST):
            portee = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=portee, comp=[])
            self.assertEqual(base.get_portee(), portee)

    def test_get_equipe(self):
        for _ in range(BOUCLE_TEST):
            equipe = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=equipe,
                        combat=0, demolition=0, degradation=0, portee=0, comp=[])
            self.assertEqual(base.get_equipe(), equipe)

    def test_get_combat(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=combat,
                        demolition=0, degradation=0, portee=0, comp=[])
            self.assertEqual(base.get_combat(), combat)

    def test_get_demolition(self):
        for _ in range(BOUCLE_TEST):
            demolition = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=demolition, degradation=0, portee=0, comp=[])
            self.assertEqual(base.get_demolition(), demolition)

    def test_get_degradation(self):
        for _ in range(BOUCLE_TEST):
            degradation = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=degradation, portee=0, comp=[])
            self.assertEqual(base.get_degradation(), degradation)

    def test_get_comp(self):
        """ Pas implémenté """
        self.skipTest("Pas implémenté")

    def test_set_nom(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_nom(nom)
            self.assertEqual(base.get_nom(), nom)

    def test_set_pos(self):
        for _ in range(BOUCLE_TEST):
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_pos(pos)
            self.assertEqual(base.get_pos(), pos)

    def test_set_cout(self):
        for _ in range(BOUCLE_TEST):
            cout = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_cout(cout)
            self.assertEqual(base.get_cout(), cout)

    def test_set_portee(self):
        for _ in range(BOUCLE_TEST):
            portee = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_portee(portee)
            self.assertEqual(base.get_portee(), portee)

    def test_set_equipe(self):
        for _ in range(BOUCLE_TEST):
            equipe = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_equipe(equipe)
            self.assertEqual(base.get_equipe(), equipe)

    def test_set_combat(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_combat(combat)
            self.assertEqual(base.get_combat(), combat)

    def test_set_demolition(self):
        for _ in range(BOUCLE_TEST):
            demolition = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_demolition(demolition)
            self.assertEqual(base.get_demolition(), demolition)

    def test_set_degradation(self):
        for _ in range(BOUCLE_TEST):
            degradation = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, combat=0,
                        demolition=0, degradation=0, portee=0, comp=[])
            base.set_degradation(degradation)
            self.assertEqual(base.get_degradation(), degradation)

    def test_set_comp(self):
        """ Pas implémenté """
        self.skipTest("Pas implémenté")

    def test_ajouter_competence(self):
        """ Pas implémenté """
        self.skipTest("Pas implémenté")

    def test_retirer_competence(self):
        """ Pas implémenté """
        self.skipTest("Pas implémenté")


if __name__ == '__main__':
    unittest.main()

""" Fichier de tests de la classe Sort """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.sort import Sort
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestSort(unittest.TestCase):
    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            Sort(nom=nom, pos=pos, cout=cout, equipe=equipe, comp=[])

    def test_est_sort(self):
        for _ in range(BOUCLE_TEST):
            sort = Sort(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            self.assertTrue(sort.est_sort())

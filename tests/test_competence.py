""" Fichier de test de la classe Competence """

# pylint: disable=missing-function-docstring, missing-class-docstring

import unittest
from random import randint, choice
from src.competences import Competence
from src.phase import PhaseTour
from tests.utils import MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR, generate_random_string


class TestCompetence(unittest.TestCase):
    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            duree = randint(MIN_INT, MAX_INT)
            nom = generate_random_string(TAILLE_STR)
            phase = choice(list(PhaseTour))
            Competence(duree=duree, nom_effet=nom, phase=phase)

    def test_get_duree(self):
        for _ in range(BOUCLE_TEST):
            duree = randint(MIN_INT, MAX_INT)
            competence = Competence(
                duree=duree, nom_effet="", phase=choice(list(PhaseTour)))
            self.assertEqual(competence.get_duree(), duree)

    def test_get_phase(self):
        for _ in range(BOUCLE_TEST):
            phase = choice(list(PhaseTour))
            competence = Competence(duree=0, nom_effet="", phase=phase)
            self.assertEqual(competence.get_phase(), phase)

    def test_appliquer_effet(self):
        """ Pas implémenté """ #TODO: Implémenter
        self.skipTest("Pas implémenté")

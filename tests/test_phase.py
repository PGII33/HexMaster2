""" Fichier de test pour la classe PhaseTour """

# pylint: disable=missing-function-docstring, missing-class-docstring

import unittest
from src.phase import PhaseTour


class TestPhaseTour(unittest.TestCase):

    def test_enum_unicite(self):
        phases = list(PhaseTour)
        valeurs = [phase.value for phase in phases]
        for val in valeurs:
            self.assertEqual(valeurs.count(
                val), 1, f"La valeur {val} est dupliquée dans l'enum PhaseTour")

    def test_enum_type(self):
        for phase in PhaseTour:
            self.assertIsInstance(
                phase.value, int, f"La valeur de {phase.name} n'est pas un entier")

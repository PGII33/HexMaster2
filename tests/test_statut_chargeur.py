"""Tests du chargement des statuts."""

import unittest

from src.chargeur.statut_chargeur import StatutChargeur
from src.effets import Effet
from src.statut import StatutActif
from src.creature import Creature
from src.case import Case


class TestStatutChargeur(unittest.TestCase):
    def test_charger_et_creer_statut_depuis_id(self):
        chargeur = StatutChargeur()
        chargeur.charger_statut("data/statuts/mouille.json")
        StatutActif.enregistrer_statuts_custom(chargeur.statuts_chargees)

        statut = StatutActif.depuis_id("mouille")

        self.assertEqual(statut.get_id(), "mouille")
        self.assertEqual(statut.get_nom(), "Mouille")
        self.assertEqual(statut.get_duree_restante(), 3)
        self.assertEqual(statut.get_modificateur("mouv_max"), -1)
        self.assertFalse(statut.est_buff())

    def test_donner_statut_sur_cible(self):
        chargeur = StatutChargeur()
        chargeur.charger_statut("data/statuts/mouille.json")
        StatutActif.enregistrer_statuts_custom(chargeur.statuts_chargees)

        origine = Creature(pv=5, nom="origine", cout=0, pos=(0, 0), equipe=0,
                           combat=0, demolition=0, degradation=0, portee=0,
                           control=0, mouv=2)
        cible = Creature(pv=5, nom="cible", cout=0, pos=(0, 0), equipe=1,
                         combat=0, demolition=0, degradation=0, portee=0,
                         control=0, mouv=2)
        case = Case(pv=10, nom="case", pos=(0, 0), cout=0, equipe=0,
                    control=0, control_max=10, comp=[])

        Effet.donner_statut(origine, [origine, cible, case], "mouille", cible, sur="cible")

        self.assertIsNotNone(cible.get_statut("mouille"))
        self.assertEqual(cible.get_statut("mouille").get_duree_restante(), 3)
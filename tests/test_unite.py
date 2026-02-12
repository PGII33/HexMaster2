""" Fichier de tests de la classe Unite """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.unite import Unite
from src.creature import Creature
from src.batiment import Batiment
from src.case import Case
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestUnite(unittest.TestCase):

    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            pv = randint(MIN_INT, MAX_INT)
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            ctrl = randint(MIN_INT, MAX_INT)
            combat = randint(MIN_INT, MAX_INT)
            demolition = randint(MIN_INT, MAX_INT)
            degradation = randint(MIN_INT, MAX_INT)
            portee = randint(MIN_INT, MAX_INT)
            Unite(pv=pv, nom=nom, pos=pos, cout=cout, equipe=equipe, control=ctrl,
                  combat=combat, demolition=demolition, degradation=degradation, portee=portee)

    def test_attaquer(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(0, int(MAX_INT/2)) # Choix arbitraire pour pouvoir
                                           # trouver facilement des valeurs au dessus
            demolition = randint(0, int(MAX_INT/2))
            degradation = randint(0, int(MAX_INT/2))
            pv = randint(max(combat, demolition, degradation), MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=combat, demolition=demolition, degradation=degradation, portee=1)
            cible_creature = Creature(pv=pv, nom="", cout=0, pos=(1, 0), equipe=1, control=0,
                                      combat=0, demolition=0, degradation=0, portee=0, mouv=0)
            cible_batiment = Batiment(pv=pv, nom="", cout=0, pos=(0, -1), equipe=1, control=0,
                                      combat=0, demolition=0, degradation=0, portee=0)
            cible_case = Case(pv=pv, pos=(0, 0), equipe=1, control_max=0, nom="", cout=0)
            cible_case_pas_a_portee = Case(pv=pv, pos=(93, 0), equipe=1, control_max=0, nom="", cout=0)
            cible_unite = Unite(pv=pv, nom="", cout=0, pos=(0, 0), equipe=1, control=0,
                                   combat=0, demolition=0, degradation=0, portee=0)
            unite.attaquer(cible_creature)
            unite.attaquer(cible_batiment)
            unite.attaquer(cible_case)
            unite.attaquer(cible_case_pas_a_portee)
            unite.attaquer(cible_unite)

            self.assertEqual(cible_creature.get_pv(), pv - combat,
                             f"PV de la créature incorrect après attaque, combat={combat}, pv_initiaux={pv}"+
                             f"pv_attendus={pv - combat}, pv_obtenus={cible_creature.get_pv()}")
            self.assertEqual(cible_batiment.get_pv(), pv - demolition,
                                f"PV du bâtiment incorrect après attaque, demolition={demolition}, pv_initiaux={pv}"+
                                f"pv_attendus={pv - demolition}, pv_obtenus={cible_batiment.get_pv()}")
            self.assertEqual(cible_case.get_pv(), pv - degradation,
                                f"PV de la case incorrect après attaque, degradation={degradation}, pv_initiaux={pv}"+
                                f"pv_attendus={pv - degradation}, pv_obtenus={cible_case.get_pv()}")
            self.assertEqual(cible_case_pas_a_portee.get_pv(), pv,
                                "La cible n'était pas à portée mais a quand même pris des dégats")
            self.assertEqual(cible_unite.get_pv(), pv,
                                "Une unité n'est pas censé pouvoir attaquer autre chose qu'une créature,"+
                                " un bâtiment ou une case, mais ici, elle a pu attaquer une autre unite"+
                                f" pv_initiaux={pv}, pv_obtenus={cible_unite.get_pv()}, combat={combat}," +
                                f" demolition={demolition}, degradation={degradation}")

    def test_fin_tour(self):
        for _ in range(BOUCLE_TEST):
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_a_attaque(True)
            unite.fin_tour()
            self.assertFalse(unite.get_a_attaque())

    def test_get_a_attaque(self):
        for _ in range(BOUCLE_TEST):
            a_attaque = randint(0, 1)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_a_attaque(a_attaque)
            self.assertEqual(unite.get_a_attaque(), a_attaque)

    def test_set_a_attaque(self):
        for _ in range(BOUCLE_TEST):
            a_attaque = randint(0, 1)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_a_attaque(a_attaque)
            self.assertEqual(unite.get_a_attaque(), a_attaque)

    def test_get_combat(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=combat, demolition=0, degradation=0, portee=0)
            self.assertEqual(unite.get_combat(), combat)

    def test_set_combat(self):
        for _ in range(BOUCLE_TEST):
            combat = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_combat(combat)
            self.assertEqual(unite.get_combat(), combat)

    def test_get_demolition(self):
        for _ in range(BOUCLE_TEST):
            demolition = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=demolition, degradation=0, portee=0)
            self.assertEqual(unite.get_demolition(), demolition)

    def test_set_demolition(self):
        for _ in range(BOUCLE_TEST):
            demolition = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_demolition(demolition)
            self.assertEqual(unite.get_demolition(), demolition)

    def test_get_degradation(self):
        for _ in range(BOUCLE_TEST):
            degradation = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=degradation, portee=0)
            self.assertEqual(unite.get_degradation(), degradation)

    def test_set_degradation(self):
        for _ in range(BOUCLE_TEST):
            degradation = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_degradation(degradation)
            self.assertEqual(unite.get_degradation(), degradation)

    def test_get_portee(self):
        for _ in range(BOUCLE_TEST):
            portee = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=portee)
            self.assertEqual(unite.get_portee(), portee)

    def test_set_portee(self):
        for _ in range(BOUCLE_TEST):
            portee = randint(MIN_INT, MAX_INT)
            unite = Unite(pv=0, nom="", cout=0, pos=(0, 0), equipe=0, control=0,
                          combat=0, demolition=0, degradation=0, portee=0)
            unite.set_portee(portee)
            self.assertEqual(unite.get_portee(), portee)

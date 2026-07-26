""" Fichier de tests de la classe Creature """

#pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint
import unittest
from src.creature import Creature
from src.effets import Effet
from src.statut import StatutActif
from src.chargeur.statut_chargeur import StatutChargeur
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR

class TestCreature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chargeur = StatutChargeur()
        chargeur.charger_tous_les_statuts()
        StatutActif.enregistrer_statuts_custom(chargeur.statuts_chargees)

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

    def test_get_mouv_max(self):
        for _ in range(BOUCLE_TEST):
            mouv = randint(MIN_INT, MAX_INT)
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=mouv)
            self.assertEqual(creature.get_mouv_max(), mouv)

    def test_get_mal_invocation(self):
        values = [True, False]
        for v in values:
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=0)
            creature.set_mal_invocation(v)
            self.assertEqual(creature.get_mal_invocation(), v)

    def test_set_mal_invocation(self):
        values = [True, False]
        for v1 in values:
            for v2 in values:
                creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                    combat=0, demolition=0, degradation=0, portee=0,
                                    control=0, mouv=0)
                creature.set_mal_invocation(v1)
                self.assertEqual(creature.get_mal_invocation(), v1)
                creature.set_mal_invocation(v2)
                self.assertEqual(creature.get_mal_invocation(), v2)

    def test_est_creature(self):
        for _ in range(BOUCLE_TEST):
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=0)
            self.assertTrue(creature.est_creature())

    def test_debut_tour(self):
        for _ in range(BOUCLE_TEST):
            mouv=randint(1, MAX_INT)
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=mouv)
            creature.set_mouv(mouv-randint(1, mouv))
            creature.debut_tour()
            self.assertEqual(creature.get_mouv(), creature.mouv)

    def test_fin_tour(self):
        for _ in range(BOUCLE_TEST):
            creature = Creature(pv=0, nom="", cout=0, pos=(0, 0), equipe=0,
                                combat=0, demolition=0, degradation=0, portee=0,
                                control=0, mouv=randint(MIN_INT, MAX_INT))
            creature.fin_tour()
            self.assertFalse(creature.get_mal_invocation())

    def test_mouille_reduit_mouvement_max(self):
        creature = Creature(pv=5, nom="", cout=0, pos=(0, 0), equipe=0,
                            combat=0, demolition=0, degradation=0, portee=0,
                            control=0, mouv=2)

        creature.ajouter_statut(Effet._creer_statut_depuis_id("mouille"))

        self.assertEqual(creature.get_mouv_max(), 1)
        self.assertEqual(creature.get_mouv(), 1)

    def test_retirer_mouille_restaure_mouvement_max(self):
        creature = Creature(pv=5, nom="", cout=0, pos=(0, 0), equipe=0,
                            combat=0, demolition=0, degradation=0, portee=0,
                            control=0, mouv=2)

        creature.ajouter_statut(Effet._creer_statut_depuis_id("mouille"))
        creature.retirer_statut("Mouille")

        self.assertEqual(creature.get_mouv_max(), 2)
        self.assertEqual(creature.get_mouv(), 2)

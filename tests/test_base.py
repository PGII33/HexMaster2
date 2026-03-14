""" Fichier de tests de la classe Base """

# pylint: disable=missing-function-docstring, missing-class-docstring

from random import randint, choice
import unittest
from src.base import Base
from src.competence import Competence
from src.phase import PhaseTour
from src.tag import TagActif
from tests.utils import generate_random_string, MIN_INT, MAX_INT, BOUCLE_TEST, TAILLE_STR


class TestBase(unittest.TestCase):
    def test__init__(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            cout = randint(MIN_INT, MAX_INT)
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            equipe = randint(MIN_INT, MAX_INT)
            Base(nom=nom, pos=pos, cout=cout, equipe=equipe, comp=[])

    def test_get_nom(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            base = Base(nom=nom, pos=(0, 0), cout=0, equipe=0, comp=[])
            self.assertEqual(base.get_nom(), nom)

    def test_set_nom(self):
        for _ in range(BOUCLE_TEST):
            nom = generate_random_string(TAILLE_STR)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            base.set_nom(nom)
            self.assertEqual(base.get_nom(), nom)

    def test_get_pos(self):
        for _ in range(BOUCLE_TEST):
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            base = Base(nom="", pos=pos, cout=0, equipe=0, comp=[])
            self.assertEqual(base.get_pos(), pos)

    def test_set_pos(self):
        for _ in range(BOUCLE_TEST):
            pos = (randint(MIN_INT, MAX_INT), randint(MIN_INT, MAX_INT))
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            base.set_pos(pos)
            self.assertEqual(base.get_pos(), pos)

    def test_get_cout(self):
        for _ in range(BOUCLE_TEST):
            cout = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=cout, equipe=0, comp=[])
            self.assertEqual(base.get_cout(), cout)

    def test_set_cout(self):
        for _ in range(BOUCLE_TEST):
            cout = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            base.set_cout(cout)
            self.assertEqual(base.get_cout(), cout)

    def test_get_equipe(self):
        for _ in range(BOUCLE_TEST):
            equipe = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=equipe, comp=[])
            self.assertEqual(base.get_equipe(), equipe)

    def test_set_equipe(self):
        for _ in range(BOUCLE_TEST):
            equipe = randint(MIN_INT, MAX_INT)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            base.set_equipe(equipe)
            self.assertEqual(base.get_equipe(), equipe)

    def test_get_comp(self):
        for _ in range(BOUCLE_TEST):
            noms_comp = [generate_random_string(TAILLE_STR) for _ in range(BOUCLE_TEST)]
            comp = [Competence(duree=0, nom_effet=nom, phase=choice(list(PhaseTour))) for nom in noms_comp]
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=comp)
            self.assertEqual(base.get_comp(), comp)

    def test_set_comp(self):
        for _ in range(BOUCLE_TEST):
            noms_comp = [generate_random_string(TAILLE_STR) for _ in range(BOUCLE_TEST)]
            comp = [Competence(duree=0, nom_effet=nom, phase=choice(list(PhaseTour))) for nom in noms_comp]
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            base.set_comp(comp)
            self.assertEqual(base.get_comp(), comp)

    def test_ajouter_competence(self):
        for _ in range(BOUCLE_TEST):
            nom_comp = generate_random_string(TAILLE_STR)
            comp = Competence(duree=0, nom_effet=nom_comp, phase=choice(list(PhaseTour)))
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            base.ajouter_competence(comp)
            self.assertIn(comp, base.get_comp())

    def test_retirer_competence(self):
        for _ in range(BOUCLE_TEST):
            comps = []
            rng = randint(1, BOUCLE_TEST)
            for _ in range(rng):
                nom_comp = generate_random_string(TAILLE_STR)
                comp = Competence(duree=0, nom_effet=nom_comp, phase=choice(list(PhaseTour)))
                comps.append(comp)

            nom_comp_qui_existe_pas = generate_random_string(max(1, TAILLE_STR-1)) # Si pas la même taille alors différent
            comp_qui_existe_pas = Competence(duree=0, nom_effet=nom_comp_qui_existe_pas, phase=choice(list(PhaseTour)))
            comp = choice(comps)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=comps)

            base.retirer_competence(comp_qui_existe_pas)
            self.assertNotIn(comp_qui_existe_pas, base.get_comp())

            for comp in comps:
                self.assertIn(comp, base.get_comp())

            base.retirer_competence(comp)
            self.assertNotIn(comp, base.get_comp())

    def test_ajouter_tag_rafraichit_existant(self):
        base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])

        base.ajouter_tag(TagActif("Mouille", 1, modificateurs={"mouv_max": -1}))
        base.ajouter_tag(TagActif("Mouille", 3, modificateurs={"mouv_max": -1}))

        self.assertEqual(len(base.get_tags()), 1)
        self.assertEqual(base.get_tag("mouille").get_duree_restante(), 3)

    def test_retirer_tag(self):
        base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])

        base.ajouter_tag(TagActif("Mouille", 3, modificateurs={"mouv_max": -1}))
        base.retirer_tag("Mouille")

        self.assertIsNone(base.get_tag("Mouille"))
        self.assertEqual(base.get_tags(), [])


    def test_get_carte_path(self):
        for _ in range(BOUCLE_TEST):
            path = generate_random_string(TAILLE_STR)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[], carte_path=path)
            self.assertEqual(base.get_carte_path(), path)

    def test_get_sprite_path(self):
        for _ in range(BOUCLE_TEST):
            path = generate_random_string(TAILLE_STR)
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[], sprite_path=path)
            self.assertEqual(base.get_sprite_path(), path)

    def test_est_batiment(self):
        for _ in range(BOUCLE_TEST):
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            self.assertFalse(base.est_batiment())

    def test_est_case(self):
        for _ in range(BOUCLE_TEST):
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            self.assertFalse(base.est_case())

    def test_est_creature(self):
        for _ in range(BOUCLE_TEST):
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            self.assertFalse(base.est_creature())

    def test_est_sort(self):
        for _ in range(BOUCLE_TEST):
            base = Base(nom="", pos=(0, 0), cout=0, equipe=0, comp=[])
            self.assertFalse(base.est_sort())

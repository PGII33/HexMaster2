""" Gestion d'un Deck """
import random
from src.const import TAILLE_MAIN_MAX


class Deck:
    """ Deck du joueur, composé de 10 cartes au total """

    def __init__(self, definitions: list, chargeur):
        """ Initialise le deck avec les définitions des cartes

        Args:
            definitions: Liste de tuples (id_entite, equipe) pour chaque carte
            chargeur: Instance d'EntiteChargeur pour recréer les cartes
        """
        self.definitions = definitions.copy()  # Liste des (id, equipe)
        self.chargeur = chargeur
        self.cartes = []
        self.reinitialiser()

    def reinitialiser(self):
        """ Réinitialise le deck en recréant toutes les instances """
        self.cartes = [self.chargeur.creer_instance(id_entite, None, equipe)
                       for id_entite, equipe in self.definitions]
        self.melanger()

    def melanger(self):
        """ Mélange le deck """
        random.shuffle(self.cartes)

    def piocher(self):
        """ Pioche une carte du deck """
        if len(self.cartes) == 0:
            self.reinitialiser()
        return self.cartes.pop()


class Main:
    """ Main du joueur, composée de 4 au maximum """

    def __init__(self):
        self.cartes = []

    def ajouter_carte(self, carte):
        """ Ajoute une carte à la main """
        if len(self.cartes) < TAILLE_MAIN_MAX:
            self.cartes.append(carte)

    def retirer_carte(self, carte):
        """ Retire une carte de la main """
        self.cartes.remove(carte)

    def get_cartes(self):
        """ Renvoie les cartes de la main """
        return self.cartes

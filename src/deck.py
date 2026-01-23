""" Gestion d'un Deck """
import random

class Deck:
    """ Deck du joueur, composé de 10 cartes au total """
    def __init__(self, cartes:list):
        self.liste_cartes = cartes
        self.cartes = cartes

    def reinitialiser(self):
        """ Réinitialise le deck """
        self.cartes = self.liste_cartes.copy()

    def melanger(self):
        """ Mélange le deck """
        random.shuffle(self.cartes)

    def piocher(self):
        """ Pioche une carte du deck """
        carte =  self.cartes.pop()
        if len(self.cartes) == 0:
            self.reinitialiser()
        return carte


class Main:
    """ Main du joueur, composée de 4 au maximum """
    def __init__(self):
        self.cartes = []

    def ajouter_carte(self, carte):
        """ Ajoute une carte à la main """
        if len(self.cartes) < 4:
            self.cartes.append(carte)

    def retirer_carte(self, carte):
        """ Retire une carte de la main """
        self.cartes.remove(carte)

    def get_cartes(self):
        """ Renvoie les cartes de la main """
        return self.cartes

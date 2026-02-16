""" Gestion d'un joueur """
from src.deck import Deck
from src.deck import Main
from src.const import TAILLE_MAIN_MAX


class Joueur:
    """ Un joueur dans une partie """

    def __init__(self, nom: str, deck: Deck, pi: int, equipe: int):
        self.nom = nom
        self.deck = deck
        self.pi = pi  # points d'invocation
        self.equipe = equipe
        self.main = Main()

    def get_nom(self) -> str:
        """ Renvoie le nom du joueur """
        return self.nom

    def set_nom(self, nom: str):
        """ Change le nom du joueur """
        self.nom = nom

    def get_deck(self) -> Deck:
        """ Renvoie le deck """
        return self.deck

    def set_deck(self, deck: Deck):
        """ Change le deck """
        self.deck = deck

    def get_main(self) -> Main:
        """ Renvoie la main """
        return self.main

    def get_pi(self) -> int:
        """ Renvoie les points d'invocation """
        return self.pi

    def set_pi(self, pi: int):
        """ Change les points d'invocation """
        self.pi = pi

    def get_equipe(self) -> int:
        """ Renvoie l'équipe du joueur """
        return self.equipe

    def piocher_cartes(self):
        """ Pioche des cartes : 4 si main vide, sinon 1 par tour (jusqu'à maximum 4) """

        if len(self.get_main().get_cartes()) == 0:
            for _ in range(min(TAILLE_MAIN_MAX, len(self.get_deck().definitions))):
                if len(self.get_main().get_cartes()) < TAILLE_MAIN_MAX:
                    carte = self.get_deck().piocher()
                    self.get_main().ajouter_carte(carte)

        elif len(self.get_main().get_cartes()) < TAILLE_MAIN_MAX:
            carte = self.get_deck().piocher()
            self.get_main().ajouter_carte(carte)

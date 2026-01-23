""" Gestion d'un joueur """
from src.deck import Deck
from src.deck import Main

class Joueur:
    """ Un joueur dans une partie """
    def __init__(self, nom:str, deck:Deck, pi:int, numero:int):
        self.nom = nom
        self.deck = deck
        self.pi = pi # points d'invocation
        self.numero = numero
        self.main = Main()

    def get_nom(self) -> str:
        """ Renvoie le nom du joueur """
        return self.nom

    def get_deck(self) -> Deck:
        """ Renvoie le deck """
        return self.deck

    def get_main(self)-> Main:
        """ Renvoie la main """
        return self.main

    def get_pi(self) -> int:
        """ Renvoie les points d'invocation """
        return self.pi

    def get_numero(self) -> int:
        """ Renvoie l'identifiant du joueur (son numero) """
        return self.numero

    def set_nom(self, nom:str):
        """ Change le nom du joueur """
        self.nom = nom

    def set_main(self, main:Main):
        """ Change la main """
        self.main = main

    def set_deck(self, deck:Deck):
        """ Change le deck """
        self.deck = deck

    def set_pi(self, pi:int):
        """ Change les points d'invocation """
        self.pi = pi

    def tour(self):
        """ Gère un tour du joueur """
        while len(self.get_main().get_cartes()) < 4:
            carte = self.get_deck().piocher()
            self.get_main().ajouter_carte(carte)
        for carte in self.main.get_cartes():
            carte.print()
        

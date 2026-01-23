""" Classe de gestion du terrain, l'ensemble des entites presentes sur une grille """

class Terrain:
    """ Classe representant le terrain de jeu """
    def __init__(self, entites:list):
        """ Initialise le terrain """
        self.entites = entites  # Liste des entites presentes sur le terrain

    def get_entites(self) -> list:
        """ Retourne la liste des entites presentes sur le terrain """
        return self.entites

    def debut_tour(self, joueur_actif:int):
        """ Gère le début du tour pour les entites du terrain """
        for entite in self.entites:
            if entite.get_equipe() == joueur_actif:
                entite.debut_tour()

    def fin_tour(self, joueur_actif:int):
        """ Gère la fin du tour pour les entites du terrain """
        for entite in self.entites:
            if entite.get_equipe() == joueur_actif:
                entite.fin_tour()

    def print_entites(self):
        """ Affiche les entites presentes sur le terrain """
        for entite in self.entites:
            print(entite.get_nom(), entite.get_pos())

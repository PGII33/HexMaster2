""" Fichier de jeu """
from random import choice
from src.joueur import Joueur
from src.terrain import Terrain
from src.const import PI_TOUR

PRINT = True

class Classique:
    """ Mode de jeu classique (ratio de cases ou tuer les bâtiments et créatures adverses) """
    def __init__(self, joueurs:list[Joueur], terrain:Terrain, ratio_cases:float=1/2):
        self.joueurs = joueurs
        self.terrain = terrain
        self.ratio_cases = ratio_cases
        self.joueur_actif = choice(self.joueurs)

    def get_joueurs(self) -> list:
        """ Renvoie la liste des joueurs """
        return self.joueurs

    def get_terrain(self) -> Terrain:
        """ Renvoie le terrain """
        return self.terrain

    def get_ratio_cases(self) -> float:
        """ Renvoie le ratio de cases """
        return self.ratio_cases

    def tour(self):
        """ Gère un tour de jeu """
        # Si il y a un gagnant, le retourne
        gagnant = self.partie_terminee()
        if gagnant:
            return gagnant

        for joueur in self.joueurs:
            # Logique de tour pour chaque joueur
            joueur.set_pi(joueur.get_pi() + PI_TOUR)
            if PRINT:
                print(f"Tour du joueur {joueur.get_nom()} (PI: {joueur.get_pi()})")
            self.terrain.debut_tour(self.joueurs.index(joueur))
            joueur.tour()
            self.terrain.fin_tour(self.joueurs.index(joueur))

    def un_joueur_restant(self) -> bool | Joueur:
        """ Vérifie s'il ne reste qu'un seul joueur en vie """
        joueurs_en_vie = [joueur for joueur in self.joueurs
                          if any(entite.est_en_vie() for entite in self.terrain.get_entites()
                                 if entite.get_equipe() == self.joueurs.index(joueur))]
        return joueurs_en_vie[0] if len(joueurs_en_vie) == 1 else False

    def ratio_complete(self) -> bool | Joueur:
        """ Vérifie si un joueur a atteint le ratio de cases requis
        Si c'est le cas, renvoie le joueur, sinon False
        """
        total_cases = len(self.terrain.get_entites())
        for joueur in self.joueurs:
            cases_joueur = sum(1 for entite in self.terrain.get_entites()
                               if entite.get_equipe() == self.joueurs.index(joueur))
            if (cases_joueur / total_cases) >= self.ratio_cases:
                return True
        return False

    def partie_terminee(self) -> bool | Joueur:
        """ Vérifie si la partie est terminée """
        gagnant = self.un_joueur_restant()
        if gagnant:
            return gagnant
        gagnant = self.ratio_complete()
        if gagnant:
            return gagnant
        return False

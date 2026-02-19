""" Fichier de jeu """
from random import choice
from src.joueur import Joueur
from src.terrain import Terrain
from src.const import PI_TOUR


class Classique:
    """ Mode de jeu classique (ratio de cases ou tuer les bâtiments et créatures adverses) """

    def __init__(self, joueurs: list[Joueur], terrain: Terrain, ratio_cases: float = 4/5):
        self.joueurs = joueurs
        self.terrain = terrain
        self.ratio_cases = ratio_cases
        self.joueur_actif = choice(self.joueurs)

        # Créer le dictionnaire joueurs par équipe pour le terrain
        joueurs_dict = {joueur.get_equipe(): joueur for joueur in joueurs}
        self.terrain.joueurs = joueurs_dict

    def get_joueurs(self) -> list:
        """ Renvoie la liste des joueurs """
        return self.joueurs

    def get_terrain(self) -> Terrain:
        """ Renvoie le terrain """
        return self.terrain

    def get_ratio_cases(self) -> float:
        """ Renvoie le ratio de cases """
        return self.ratio_cases

    def get_entitees(self) -> list:
        """ Renvoie la liste des entités sur le terrain """
        return self.terrain.get_entites()

    def get_joueur_actif(self) -> Joueur:
        """ Renvoie le joueur actif """
        return self.joueur_actif

    def set_joueur_actif(self, joueur: Joueur):
        """ Change le joueur actif """
        self.joueur_actif = joueur

    def tour(self)-> None | Joueur:
        """ Gère un tour de jeu """
        # Si il y a un gagnant, le retourne
        gagnant = self.partie_terminee()
        if gagnant:
            return gagnant

        for joueur in self.joueurs:
            # Logique de tour pour chaque joueur
            joueur.set_pi(joueur.get_pi() + PI_TOUR)
            self.terrain.debut_tour(joueur.get_equipe())
            joueur.piocher_cartes()
            self.terrain.fin_tour(joueur.get_equipe())
        return None

    def un_joueur_restant(self) -> bool | Joueur:
        """ Vérifie s'il ne reste qu'un seul joueur en vie """
        joueurs_en_vie = [joueur for joueur in self.joueurs
                          if any(entite for entite in self.terrain.get_entites()
                                 if entite.get_equipe() == joueur.get_equipe())]
        return joueurs_en_vie[0] if len(joueurs_en_vie) == 1 else False

    def ratio_complete(self) -> bool | Joueur:
        """ Vérifie si un joueur a atteint le ratio de cases requis
        Si c'est le cas, renvoie le joueur, sinon False
        """
        total_cases = sum(
            1 for entite in self.terrain.get_entites() if entite.est_case())
        if total_cases == 0:
            return False

        for joueur in self.joueurs:
            cases_joueur = sum(1 for entite in self.terrain.get_entites()
                               if entite.est_case() and entite.get_equipe() == joueur.get_equipe())
            if (cases_joueur / total_cases) >= self.ratio_cases:
                return joueur
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

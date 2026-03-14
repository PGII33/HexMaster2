""" Classe de gestion du terrain, l'ensemble des entites presentes sur une grille """

from src.phase import PhaseTour


class Terrain:
    """ Classe representant le terrain de jeu """

    def __init__(self, entites: list, joueurs: dict = None):
        """ Initialise le terrain 

        Args:
            entites: Liste des entités présentes sur le terrain
            joueurs: Dictionnaire {numero_equipe: objet_joueur} pour les effets nécessitant les joueurs
        """
        self.entites = entites  # Liste des entites presentes sur le terrain
        # Dictionnaire des joueurs par équipe
        self.joueurs = joueurs if joueurs is not None else {}

    def get_entites(self) -> list:
        """ Retourne la liste des entites presentes sur le terrain """
        return self.entites

    def debut_tour(self, joueur_actif: int):
        """ Gère le début du tour pour les entites du terrain """

        for entite in self.entites:
            if entite.get_equipe() == joueur_actif:
                if entite.est_creature():
                    entite.debut_tour()

        # Appliquer les compétences DEBUT_TOUR
        for entite in self.entites:
            if entite.get_equipe() == joueur_actif:
                for comp in entite.get_comp():
                    if comp.get_phase() == PhaseTour.DEBUT_TOUR:
                        comp.appliquer_effet(entite, self.entites, None, self.joueurs)

        # Nettoyer les entités mortes
        self.nettoyer_entites_mortes()

    def fin_tour(self, joueur_actif: int):
        """ Gère la fin du tour pour les entites du terrain """

        for entite in self.entites:
            if entite.get_equipe() == joueur_actif:
                if entite.est_creature() :
                    entite.fin_tour()

                # Si c'est une créature ou un bâtiment, appliquer le contrôle
                if entite.est_creature() or entite.est_batiment():
                    case = self.get_case_at(entite.get_pos())
                    case.appliquer_control(
                        entite.get_control(), entite.get_equipe())

                for comp in entite.get_comp():
                    if comp.get_phase() == PhaseTour.FIN_TOUR:
                        comp.appliquer_effet(entite, self.entites, None, self.joueurs)

                entite.resoudre_tags(PhaseTour.FIN_TOUR, self.entites, self.joueurs)
                entite.decrementer_tags(PhaseTour.FIN_TOUR)

        # Nettoyer les entités mortes
        self.nettoyer_entites_mortes()

    def nettoyer_entites_mortes(self):
        """ Retire les entités mortes du terrain (PV <= 0) 

        Note: Garde les cases vivantes (PV > 0) mais retire les cases mortes
        """
        self.entites = [e for e in self.entites if e.get_pv() > 0]

    def get_case_at(self, pos: tuple[int, int]):
        """ Retourne la case à une position donnée """
        for entite in self.entites:
            if entite.est_case() and entite.get_pos() == pos:
                return entite
        return None

    def avant_attaque(self, attaquant, cible):
        """ Actions a effectuer avant une attaque """
        # Appliquer les compétences passives avant l'attaque

        for c in attaquant.comp:
            if c.get_phase() == PhaseTour.AVANT_ATTAQUE:
                c.appliquer_effet(attaquant, self.entites, cible)

    def apres_attaque(self, attaquant, cible):
        """ Actions a effectuer apres une attaque """
        # Appliquer les compétences passives après l'attaque

        for c in attaquant.comp:
            if c.get_phase() == PhaseTour.APRES_ATTAQUE:
                c.appliquer_effet(attaquant, self.entites, cible, self.joueurs)

    def effectuer_attaque(self, attaquant, cible):
        """ Effectue une attaque d'un attaquant sur une cible

        Args:
            attaquant: Entité qui attaque (Creature ou Batiment)
            cible: Entité qui subit l'attaque (Creature, Batiment ou Case)
        """
        # Appliquer les compétences avant l'attaque
        if hasattr(attaquant, 'comp') and attaquant.comp:
            self.avant_attaque(attaquant, cible)

        # Effectuer l'attaque
        attaquant.attaquer(cible)

        # Appliquer les compétences après l'attaque
        if hasattr(attaquant, 'comp') and attaquant.comp:
            self.apres_attaque(attaquant, cible)

        # Nettoyer les entités mortes après l'attaque
        self.nettoyer_entites_mortes()

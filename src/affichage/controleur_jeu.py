""" Contrôleur du jeu """

from src.auxiliaire import (
    get_cases_deplacement,
    get_entites_a_portee,
    distance_hex,
    adjacents_hex
)
from src.const import PI_TOUR


class ControleurJeu:
    """ Controleur du jeu """

    def __init__(self, jeu):
        self.jeu = jeu

        # État de sélection
        self.entite_selectionnee = None
        self.cases_deplacement = []
        self.entites_a_portee = []
        self.carte_selectionnee = None

        # État de partie
        self.partie_terminee = False
        self.joueur_gagnant = None

    def traiter_selection(self, coord_hex, shift=False, ctrl=False):
        """ Traite une sélection sur le terrain """
        force_case = shift
        force_attaque = ctrl

        # Si une carte est sélectionnée, tenter l'invocation au lieu de sélectionner
        if self.carte_selectionnee:
            self._invoquer_carte(coord_hex)
            return

        # Si une entité est sélectionnée et ctrl pressé, tenter l'attaque
        if self.entite_selectionnee and force_attaque and self.entites_a_portee:
            cible = self._chercher_entite_at(coord_hex, self.entites_a_portee)
            if cible:
                self._attaquer_cible(cible)
                return

        # Sinon, sélectionner l'entité/case cliquée
        self._selectionner_entite(coord_hex, force_case)

    def selectionner_carte(self, carte):
        """ Sélectionne une carte de la main. """
        self.carte_selectionnee = carte
        self.entite_selectionnee = None
        self.cases_deplacement = []
        self.entites_a_portee = []

    def desselectionner_tout(self):
        """Réinitialise toutes les sélections."""
        self.entite_selectionnee = None
        self.carte_selectionnee = None
        self.cases_deplacement = []
        self.entites_a_portee = []

    def deplacer_vers(self, destination: tuple[int, int]):
        """ Déplace la créature sélectionnée vers la destination. """
        # Vérifier qu'une créature est sélectionnée
        if not self.entite_selectionnee or not self.entite_selectionnee.est_creature():
            return

        # Vérifier que la créature appartient au joueur actif
        joueur_actif = self.jeu.get_joueur_actif()
        if self.entite_selectionnee.get_equipe() != joueur_actif.get_equipe():
            return

        # Vérifier que la destination est accessible
        if destination not in self.cases_deplacement:
            return

        # Calculer et appliquer le déplacement
        distance = distance_hex(self.entite_selectionnee.get_pos(), destination)
        self.entite_selectionnee.set_pos(destination)

        # Réduire les points de mouvement
        mouv_restant = self.entite_selectionnee.get_mouv() - distance
        self.entite_selectionnee.set_mouv(max(0, mouv_restant))

        # Un seul point d'entrée pour garder les overlays cohérents.
        self._recalculer_overlays()

    def fin_de_tour(self):
        """Passe au joueur suivant et gère la transition."""
        joueurs = self.jeu.get_joueurs()
        joueur_actuel = self.jeu.get_joueur_actif()
        index_actuel = joueurs.index(joueur_actuel)
        prochain_index = (index_actuel + 1) % len(joueurs)

        # Fin de tour du joueur actuel
        self.jeu.get_terrain().fin_tour(joueur_actuel.get_equipe())

        # Début de tour du prochain joueur
        joueur_suivant = joueurs[prochain_index]
        self.jeu.set_joueur_actif(joueur_suivant)
        self.jeu.get_terrain().debut_tour(joueur_suivant.get_equipe())

        # Ajouter les PI au joueur
        joueur_suivant.set_pi(joueur_suivant.get_pi() + PI_TOUR)

        # Piocher 1 carte par tour (jusqu'à maximum 4)
        joueur_suivant.piocher_cartes()

        # Vérifier les conditions de victoire
        gagnant = self.jeu.partie_terminee()
        if gagnant:
            self.partie_terminee = True
            self.joueur_gagnant = gagnant

        self.desselectionner_tout()

    def _selectionner_entite(self, coord_hex, force_case=False):
        """ Sélectionne une entité ou case à la position donnée. """
        self.entite_selectionnee = None

        if force_case:
            # Shift+clic : sélectionner uniquement les cases
            for entite in self.jeu.get_entitees():
                if entite.get_pos() == coord_hex and entite.est_case():
                    self.entite_selectionnee = entite
                    break
        else:
            # Clic normal : priorité aux créatures/bâtiments, puis cases
            case_trouvee = None
            for entite in self.jeu.get_entitees():
                if entite.get_pos() == coord_hex:
                    if not entite.est_case():
                        self.entite_selectionnee = entite
                        break
                    elif case_trouvee is None:
                        case_trouvee = entite

            # Si aucune non-case trouvée, utiliser la case
            if not self.entite_selectionnee and case_trouvee:
                self.entite_selectionnee = case_trouvee

        # Recalculer les overlays de déplacement et attaque
        self._recalculer_overlays()

        # Désélectionner la carte si elle était sélectionnée
        self.carte_selectionnee = None

    def _recalculer_overlays(self):
        """Recalcule les cases de déplacement et entités à portée."""
        if not self.entite_selectionnee or not self.entite_selectionnee.est_creature():
            self.cases_deplacement = []
            self.entites_a_portee = []
            return

        joueur_actif = self.jeu.get_joueur_actif()
        equipe_joueur = joueur_actif.get_equipe()

        # Vérifier que la créature appartient au joueur actif et n'a pas le mal d'invocation
        if (self.entite_selectionnee.get_equipe() == equipe_joueur
                and not self.entite_selectionnee.get_mal_invocation()):
            self.cases_deplacement = get_cases_deplacement(
                self.entite_selectionnee, self.jeu.get_terrain()
            )
            if self.entite_selectionnee.get_a_attaque():
                self.entites_a_portee = []
            else:
                self.entites_a_portee = get_entites_a_portee(
                    self.entite_selectionnee, self.jeu.get_terrain()
                )
        else:
            self.cases_deplacement = []
            self.entites_a_portee = []

    def _attaquer_cible(self, cible):
        """ Effectue une attaque avec l'entité sélectionnée. """
        if not self.entite_selectionnee:
            return

        # Vérifier que l'entité peut attaquer
        if not (self.entite_selectionnee.est_creature() or self.entite_selectionnee.est_batiment()):
            return

        # Vérifier que l'entité appartient au joueur actif
        joueur_actif = self.jeu.get_joueur_actif()
        if self.entite_selectionnee.get_equipe() != joueur_actif.get_equipe():
            return

        # Vérifier que l'entité n'a pas déjà attaqué
        if self.entite_selectionnee.a_attaque:
            return

        # Effectuer l'attaque
        self.jeu.get_terrain().effectuer_attaque(self.entite_selectionnee, cible)
        self.entite_selectionnee.set_a_attaque(True)

        # Recalculer les overlays après modification potentielle du terrain
        self._recalculer_overlays()

    def _invoquer_carte(self, position:tuple[int, int]):
        """ Invoque la carte sélectionnée à la position donnée. """
        if not self.carte_selectionnee:
            return

        joueur_actif = self.jeu.get_joueur_actif()
        equipe_joueur = joueur_actif.get_equipe()
        cible_sort = None

        # Vérifier que le joueur a assez de PI
        if joueur_actif.get_pi() < self.carte_selectionnee.get_cout():
            return

        # Vérifier les conditions selon le type de carte
        if self.carte_selectionnee.est_creature() or self.carte_selectionnee.est_batiment():
            # Créatures et bâtiments : seulement sur des cases appartenant au joueur
            case_cible = self.jeu.get_terrain().get_case_at(position)
            if not case_cible or case_cible.get_equipe() != equipe_joueur:
                return

            # Vérifier que la case n'est pas déjà occupée
            if self._est_position_occupee(position):
                return

        elif self.carte_selectionnee.est_case():
            # Cases : seulement sur position vide, adjacente à une case possédée
            if self.jeu.get_terrain().get_case_at(position):
                return

            # Vérifier qu'il y a une case adjacente appartenant au joueur
            positions_adjacentes = adjacents_hex(position)
            case_alliee_adjacente = any(
                self.jeu.get_terrain().get_case_at(pos_adj)
                and self.jeu.get_terrain().get_case_at(pos_adj).get_equipe() == equipe_joueur
                for pos_adj in positions_adjacentes
            )

            if not case_alliee_adjacente:
                return

        elif self.carte_selectionnee.est_sort():
            # Les sorts ciblent d'abord une entité non-case, puis la case
            cible_sort = self._chercher_entite_at(position, self.jeu.get_entitees())
            if not cible_sort:
                cible_sort = self.jeu.get_terrain().get_case_at(position)
            if not cible_sort:
                return

        # Dépenser les PI
        joueur_actif.set_pi(joueur_actif.get_pi() - self.carte_selectionnee.get_cout())

        carte_jouee = self.carte_selectionnee

        # Retirer la carte jouée de la main du joueur actif
        if carte_jouee in joueur_actif.get_main().get_cartes():
            joueur_actif.get_main().retirer_carte(carte_jouee)

        if carte_jouee.est_sort():
            # Les sorts sont consommés immédiatement
            for comp in carte_jouee.get_comp():
                comp.appliquer_effet(
                    carte_jouee,
                    self.jeu.get_terrain().get_entites(),
                    cible_sort,
                    self.jeu.get_terrain().joueurs
                )
            self.jeu.get_terrain().nettoyer_entites_mortes()
        else:
            # Positionner la carte
            carte_jouee.set_pos(position)

            # Activer le mal d'invocation pour les créatures
            if carte_jouee.est_creature():
                carte_jouee.set_mal_invocation(True)

            # Ajouter l'entité invoquée sur le terrain
            self.jeu.get_terrain().get_entites().append(carte_jouee)

        self.desselectionner_tout()

    def _chercher_entite_at(self, coord_hex: tuple[int, int], entites:list)-> object|None:
        """ Cherche une entité à la position donnée parmi une liste. """
        for entite in entites:
            if entite.get_pos() == coord_hex:
                # Priorité aux non-cases
                if not entite.est_case():
                    return entite
        
        # Si pas de non-case, chercher une case
        for entite in entites:
            if entite.get_pos() == coord_hex and entite.est_case():
                return entite
        
        return None

    def _est_position_occupee(self, coord_hex):
        """Vérifie si une position est occupée par une entité non-case."""
        for entite in self.jeu.get_entitees():
            if entite.get_pos() == coord_hex and not entite.est_case():
                return True
        return False

    def get_etat(self):
        """
        Retourne l'état courant pour le rendu.

        Returns:
            Dict contenant:
            - entite_selectionnee: Entité actuellement sélectionnée
            - cases_deplacement: List des cases accessibles
            - entites_a_portee: List des entités attaquables
            - carte_selectionnee: Carte sélectionnée dans la main
            - partie_terminee: Booléen
            - joueur_gagnant: Joueur gagnant (ou None)
        """
        return {
            "entite_selectionnee": self.entite_selectionnee,
            "cases_deplacement": self.cases_deplacement,
            "entites_a_portee": self.entites_a_portee,
            "carte_selectionnee": self.carte_selectionnee,
            "partie_terminee": self.partie_terminee,
            "joueur_gagnant": self.joueur_gagnant,
        }

    def is_partie_terminee(self):
        """Vérifie si la partie est terminée."""
        return self.partie_terminee

    def get_joueur_gagnant(self):
        """Retourne le joueur gagnant (ou None)."""
        return self.joueur_gagnant

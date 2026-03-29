""" orchestre l'affichage du jeu """
# pylint: disable=no-member

from src.affichage.camera import Camera
from src.affichage.rendu import Rendu
from src.affichage.gestion_d_entree import GestionEntree
from src.affichage.sprite_manager import SpriteManager
from src.affichage.hex_utilitaire import pixel_vers_hex
from src.auxiliaire import get_cases_deplacement, get_entites_a_portee, distance_hex, adjacents_hex
from src.const import PI_TOUR
import pygame

class VueJeu:
    """ Gère le jeu """

    def __init__(self, jeu, largeur=1280, hauteur=720):

        self.jeu = jeu
        self.camera = Camera(largeur, hauteur)
        self.sprite_manager = SpriteManager()
        self.rendu = Rendu(self.sprite_manager)
        self.gestion_entree = GestionEntree()

        self.rendu.calculer_zones(largeur, hauteur)

        self.running = True

        self.entite_selectionnee = None
        self.cases_deplacement = []
        self.entites_a_portee = []  # Entités attaquables
        self.carte_selectionnee = None  # Carte de la main sélectionnée
        self.partie_terminee = False
        self.joueur_gagnant = None

    def traiter_selection(self, pos_pixel, force_case=False):
        """ Convertit le clic en sélection d'entité 

        Args:
            pos_pixel: Position du clic en pixels
            force_case: Si True, sélectionne uniquement les cases (Shift+clic)
        """
        # Si le clic n'est pas dans la zone terrain
        if not self.rendu.zone_terrain.collidepoint(pos_pixel):
            self.entite_selectionnee = None
            return

        offset_x = self.rendu.zone_terrain.x + self.rendu.zone_terrain.width // 2
        offset_y = self.rendu.zone_terrain.y + self.rendu.zone_terrain.height // 2

        pos_monde = (
            pos_pixel[0] - offset_x + self.camera.pos_x,
            pos_pixel[1] - offset_y + self.camera.pos_y
        )

        # Convertion coordonnées hex
        taille_hex = self.camera.get_taille_hex_actuelle()
        coord_hex = pixel_vers_hex(pos_monde, taille_hex)

        # Chercher l'entité à cette position
        self.entite_selectionnee = None

        if force_case:
            # Shift+clic : sélectionner uniquement les cases
            for entite in self.jeu.get_entitees():
                if entite.get_pos() == coord_hex and entite.est_case():
                    self.entite_selectionnee = entite
                    break
        else:
            # Clic normal : priorité aux entités non-cases (créatures, bâtiments, sorts)
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

        # Calculer les cases de déplacement si c'est une créature du joueur actif
        if self.entite_selectionnee and self.entite_selectionnee.est_creature():
            joueur_actif = self.jeu.get_joueur_actif()
            equipe_joueur = joueur_actif.get_equipe()

            # Vérifier que la créature appartient au joueur actif et n'a pas le mal d'invocation
            if self.entite_selectionnee.get_equipe() == equipe_joueur and not self.entite_selectionnee.get_mal_invocation():
                self.cases_deplacement = get_cases_deplacement(
                    self.entite_selectionnee, self.jeu.get_terrain()
                )
            else:
                self.cases_deplacement = []
        else:
            self.cases_deplacement = []

    def deplacer_creature(self, destination):
        """ Déplace la créature sélectionnée vers une destination

        Args:
            destination: Coordonnées hex (q, r) de destination
        """
        if not self.entite_selectionnee or not self.entite_selectionnee.est_creature():
            return

        # Vérifier que la créature appartient au joueur actif
        joueur_actif = self.jeu.get_joueur_actif()
        equipe_joueur = joueur_actif.get_equipe()

        if self.entite_selectionnee.get_equipe() != equipe_joueur:
            return

        # Calculer la distance parcourue
        distance = distance_hex(
            self.entite_selectionnee.get_pos(), destination)

        # Déplacer la créature
        self.entite_selectionnee.set_pos(destination)

        # Réduire les points de mouvement
        mouv_restant = self.entite_selectionnee.get_mouv() - distance
        self.entite_selectionnee.set_mouv(max(0, mouv_restant))

        # Recalculer les cases de déplacement
        if mouv_restant > 0:
            self.cases_deplacement = get_cases_deplacement(
                self.entite_selectionnee, self.jeu.get_terrain()
            )
        else:
            self.cases_deplacement = []

    def attaquer_cible(self, cible):
        """ Attaque une cible avec l'entité sélectionnée

        Args:
            cible: Entité à attaquer (Creature, Batiment ou Case)
        """
        if not self.entite_selectionnee:
            return

        # Vérifier que l'entité peut attaquer
        if not (self.entite_selectionnee.est_creature() or self.entite_selectionnee.est_batiment()):
            return

        # Vérifier que l'entité appartient au joueur actif
        joueur_actif = self.jeu.get_joueur_actif()
        equipe_joueur = joueur_actif.get_equipe()

        if self.entite_selectionnee.get_equipe() != equipe_joueur:
            return

        # Vérifier que l'entité n'a pas déjà attaqué
        if self.entite_selectionnee.a_attaque:
            return

        # Effectuer l'attaque
        self.jeu.get_terrain().effectuer_attaque(
            self.entite_selectionnee, cible)

        # Marquer que l'attaque a été effectuée
        self.entite_selectionnee.set_a_attaque(True)

        # Recalculer les entités à portée (vide car a déjà attaqué)
        self.entites_a_portee = []

    def invoquer_carte(self, position):
        """ Invoque une carte de la main à une position donnée

        Args:
            position: Coordonnées hex (q, r) où invoquer la carte
        """
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
            if not case_cible:
                return

            if case_cible.get_equipe() != equipe_joueur:
                return

            # Vérifier que la case n'est pas déjà occupée
            for entite in self.jeu.get_entitees():
                if entite.get_pos() == position and not entite.est_case():
                    return

        elif self.carte_selectionnee.est_case():
            # Cases : seulement sur position vide, adjacente à une case possédée
            # Vérifier qu'il n'y a pas déjà une case à cette position
            case_existante = self.jeu.get_terrain().get_case_at(position)
            if case_existante:
                return

            # Vérifier qu'il y a une case adjacente appartenant au joueur
            positions_adjacentes = adjacents_hex(position)
            case_alliee_adjacente = False
            for pos_adj in positions_adjacentes:
                case_adj = self.jeu.get_terrain().get_case_at(pos_adj)
                if case_adj and case_adj.get_equipe() == equipe_joueur:
                    case_alliee_adjacente = True
                    break

            if not case_alliee_adjacente:
                return

        elif self.carte_selectionnee.est_sort():
            # Les sorts ciblent d'abord une entité non-case sur l'hex cliqué,
            # puis la case si aucune créature/bâtiment n'est présente.
            for entite in self.jeu.get_entitees():
                if entite.get_pos() == position and not entite.est_case():
                    cible_sort = entite
                    break

            if cible_sort is None:
                cible_sort = self.jeu.get_terrain().get_case_at(position)

            if not cible_sort:
                return

        # Dépenser les PI
        joueur_actif.set_pi(joueur_actif.get_pi() -
                            self.carte_selectionnee.get_cout())

        if self.carte_selectionnee.est_sort():
            # Les sorts sont consommés immédiatement et ne restent pas sur le terrain.
            for comp in self.carte_selectionnee.get_comp():
                comp.appliquer_effet(
                    self.carte_selectionnee,
                    self.jeu.get_terrain().get_entites(),
                    cible_sort,
                    self.jeu.get_terrain().joueurs
                )
            self.jeu.get_terrain().nettoyer_entites_mortes()
        else:
            # Positionner la carte
            self.carte_selectionnee.set_pos(position)

            # Activer le mal d'invocation pour les créatures
            if self.carte_selectionnee.est_creature():
                self.carte_selectionnee.set_mal_invocation(True)

            # Ajouter au terrain
            self.jeu.get_terrain().get_entites().append(self.carte_selectionnee)

        # Retirer de la main
        joueur_actif.get_main().retirer_carte(self.carte_selectionnee)

        # Réinitialiser la sélection
        self.carte_selectionnee = None

    def _gerer_evenements_systeme(self, events):
        """ Gérer les événements système """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                new_size = event.size
                largeur, hauteur = new_size
                self.rendu.calculer_zones(largeur, hauteur)
                self.camera.set_taille_ecran(largeur, hauteur)

    def _appliquer_action(self, actions):
        for action in actions:
            if action["type"] == "selection":
                force_case = action.get("shift", False)
                force_attaque = action.get("ctrl", False)

            if action["type"] == "deselection":
                # Clic droit : désélectionner tout
                self.entite_selectionnee = None
                self.carte_selectionnee = None
                self.cases_deplacement = []
                self.entites_a_portee = []

            elif action["type"] == "selection":
                # Vérifier si clic sur bouton fin de tour
                if self.rendu.bouton_fin_tour and self.rendu.bouton_fin_tour.collidepoint(action["pos_pixel"]):
                    # Changer de joueur
                    joueurs = self.jeu.get_joueurs()
                    index_actuel = joueurs.index(
                        self.jeu.get_joueur_actif())
                    prochain_index = (index_actuel + 1) % len(joueurs)

                    # Fin de tour du joueur actuel
                    joueur_actuel = self.jeu.get_joueur_actif()
                    self.jeu.get_terrain().fin_tour(joueur_actuel.get_equipe())

                    # Début de tour du prochain joueur
                    self.jeu.set_joueur_actif(joueurs[prochain_index])
                    joueur_suivant = joueurs[prochain_index]
                    self.jeu.get_terrain().debut_tour(joueur_suivant.get_equipe())

                    # Ajouter les PI au joueur
                    joueur_suivant.set_pi(
                        joueur_suivant.get_pi() + PI_TOUR)

                    # Piocher 1 carte par tour (jusqu'à maximum 4)
                    joueur_suivant.piocher_cartes()

                    # Vérifier les conditions de victoire
                    gagnant = self.jeu.partie_terminee()
                    if gagnant:
                        self.partie_terminee = True
                        self.joueur_gagnant = gagnant

                    self.entite_selectionnee = None
                    self.carte_selectionnee = None
                # Vérifier si clic sur une carte dans la main
                elif self.rendu.zone_main.collidepoint(action["pos_pixel"]):
                    carte_index = self.rendu.get_carte_cliquee(
                        action["pos_pixel"], self.jeu.get_joueur_actif())
                    if carte_index is not None:
                        cartes = self.jeu.get_joueur_actif().get_main().get_cartes()
                        self.carte_selectionnee = cartes[carte_index]
                        self.entite_selectionnee = None  # Désélectionner l'entité

                else:
                    # Shift+clic pour forcer sélection de case
                    force_case = action.get("shift", False)
                    force_attaque = action.get("ctrl", False)

                    # Si une carte est sélectionnée, tenter de l'invoquer
                    if self.carte_selectionnee and self.rendu.zone_terrain.collidepoint(action["pos_pixel"]):
                        # Convertir en coordonnées hex
                        offset_x = self.rendu.zone_terrain.x + self.rendu.zone_terrain.width // 2
                        offset_y = self.rendu.zone_terrain.y + self.rendu.zone_terrain.height // 2
                        pos_monde = (
                            action["pos_pixel"][0] -
                            offset_x + self.camera.pos_x,
                            action["pos_pixel"][1] -
                            offset_y + self.camera.pos_y
                        )
                        taille_hex = self.camera.get_taille_hex_actuelle()
                        coord_hex = pixel_vers_hex(pos_monde, taille_hex)

                        # Invoquer la carte
                        self.invoquer_carte(coord_hex)
                    # Si une entité est sélectionnée, vérifier si clic sur case de déplacement ou entité à portée
                    elif self.entite_selectionnee and not force_case:
                        # Convertir la position clic en coordonnées hex
                        offset_x = self.rendu.zone_terrain.x + self.rendu.zone_terrain.width // 2
                        offset_y = self.rendu.zone_terrain.y + self.rendu.zone_terrain.height // 2
                        pos_monde = (
                            action["pos_pixel"][0] -
                            offset_x + self.camera.pos_x,
                            action["pos_pixel"][1] -
                            offset_y + self.camera.pos_y
                        )
                        taille_hex = self.camera.get_taille_hex_actuelle()
                        coord_hex = pixel_vers_hex(pos_monde, taille_hex)

                        # Vérifier si clic sur une entité à portée (seulement si Ctrl pressé)
                        entite_cliquee = None
                        if force_attaque and self.entites_a_portee:
                            for entite in self.entites_a_portee:
                                if entite.get_pos() == coord_hex:
                                    # Priorité aux créatures/bâtiments, sinon cases
                                    if not entite.est_case():
                                        entite_cliquee = entite
                                        break
                                    elif not entite_cliquee:
                                        entite_cliquee = entite

                        if entite_cliquee:
                            # Attaquer la cible
                            self.attaquer_cible(entite_cliquee)
                        # Si c'est une créature et clic sur case de déplacement
                        elif self.entite_selectionnee.est_creature() and coord_hex in self.cases_deplacement:
                            self.deplacer_creature(coord_hex)
                        else:
                            # Sinon, sélectionner une nouvelle entité
                            self.traiter_selection(
                                action["pos_pixel"], force_case)
                    else:
                        self.traiter_selection(
                            action["pos_pixel"], force_case)

    def _maj_entites_a_portee(self):
        # Calculer les entités à portée si Ctrl est pressé
        if self.entite_selectionnee and (self.entite_selectionnee.est_creature() or self.entite_selectionnee.est_batiment()):
            if self.gestion_entree.ctrl_est_presse():
                joueur_actif = self.jeu.get_joueur_actif()
                equipe_joueur = joueur_actif.get_equipe()

                # Vérifier le mal d'invocation pour les créatures
                peut_attaquer = True
                if self.entite_selectionnee.est_creature() and self.entite_selectionnee.mal_invocation:
                    peut_attaquer = False

                if self.entite_selectionnee.get_equipe() == equipe_joueur and not self.entite_selectionnee.get_a_attaque() and peut_attaquer:
                    self.entites_a_portee = get_entites_a_portee(
                        self.entite_selectionnee, self.jeu.get_terrain()
                    )
                else:
                    self.entites_a_portee = []
            else:
                self.entites_a_portee = []
        else:
            self.entites_a_portee = []

    def _dessiner_scene(self, surface):            
        # Rendu
        surface.fill(self.rendu.couleur_fond)
        self.rendu.dessiner_tout(
            surface, self.camera,
            self.jeu.get_entitees(),
            self.jeu,
            self.entite_selectionnee,
            self.cases_deplacement,
            self.entites_a_portee,
            self.carte_selectionnee
        )

    def _dessiner_overlays_fin_partie(self, surface):
        self.rendu.dessiner_ecran_victoire(surface, self.joueur_gagnant)

    def handle_events(self, events):
        """ Gérer les événements (non utilisé actuellement) """
        self._gerer_evenements_systeme(events)
        actions = self.gestion_entree.traiter_evenements(events, self.camera)
        self._appliquer_action(actions)

    def update(self, dt):
        """ Mettre à jour l'état du jeu (non utilisé actuellement) """
        self._maj_entites_a_portee()

    def afficher(self, surface):
        """ Rendre le jeu sur la surface donnée (non utilisé actuellement) """
        self._dessiner_scene(surface)
        if self.partie_terminee:
            self._dessiner_overlays_fin_partie(surface)

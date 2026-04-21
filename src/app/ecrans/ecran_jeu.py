""" Fichier de l'écran de jeu, qui affiche le plateau et gère les interactions pendant la partie """

import pygame

from src.app.ecrans.base_ecran import BaseEcran
from src.affichage.controleur_jeu import ControleurJeu
from src.affichage.camera import Camera
from src.affichage.sprite_manager import SpriteManager
from src.affichage.rendu import Rendu
from src.affichage.gestion_entree import GestionEntree
from src.affichage.hex_utilitaire import ecran_vers_hex

class EcranJeu(BaseEcran):
    """ Ecran du jeu """
    def __init__(self, width, height, jeu, son_manager=None):
        super().__init__(width, height, son_manager)

        self.controleur = ControleurJeu(jeu)

        self.camera = Camera(width, height)
        self.sprite_manager = SpriteManager()
        self.rendu = Rendu(self.sprite_manager)
        self.rendu.calculer_zones(width, height)
        self.gestion_entree = GestionEntree()

    def _gerer_evenements_systeme(self, events: list) -> None:
        """Gère les événements système (fermeture, resize, escape)."""
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.set_prochain_ecran("accueil")
            elif event.type == pygame.VIDEORESIZE:
                largeur, hauteur = event.size
                self.rendu.calculer_zones(largeur, hauteur)
                self.camera.set_taille_ecran(largeur, hauteur)

    def _appliquer_actions(self, actions: list) -> None:
        """Applique les actions d'entrée au contrôleur métier."""
        for action in actions:
            action_type = action.get("type")

            if action_type == "deselection":
                self.controleur.desselectionner_tout()
                continue

            if action_type != "selection":
                continue

            pos_pixel = action.get("pos_pixel")
            if pos_pixel is None:
                continue

            # Clic sur bouton fin de tour
            if self.rendu.bouton_fin_tour and self.rendu.bouton_fin_tour.collidepoint(pos_pixel):
                self.controleur.fin_de_tour()
                continue

            # Clic dans la main pour sélectionner une carte
            if self.rendu.zone_main and self.rendu.zone_main.collidepoint(pos_pixel):
                index_carte = self.rendu.get_carte_cliquee(pos_pixel, self.controleur.jeu.get_joueur_actif())
                if index_carte is not None:
                    cartes = self.controleur.jeu.get_joueur_actif().get_main().get_cartes()
                    if 0 <= index_carte < len(cartes):
                        self.controleur.selectionner_carte(cartes[index_carte])
                continue

            # Le reste des actions se fait sur le terrain
            if not self.rendu.zone_terrain or not self.rendu.zone_terrain.collidepoint(pos_pixel):
                continue

            coord_hex = ecran_vers_hex(pos_pixel, self.rendu.zone_terrain, self.camera)
            ctrl_presse = bool(action.get("ctrl", False))

            # Si une créature est sélectionnée et que la destination est valide, on déplace.
            if (
                self.controleur.entite_selectionnee
                and self.controleur.entite_selectionnee.est_creature()
                and coord_hex in self.controleur.cases_deplacement
                and not ctrl_presse
                and not self.controleur.carte_selectionnee
            ):
                self.controleur.deplacer_vers(coord_hex)
                continue

            self.controleur.traiter_selection(
                coord_hex,
                shift=bool(action.get("shift", False)),
                ctrl=ctrl_presse,
            )

    def handle_events(self, events):
        self._gerer_evenements_systeme(events)
        actions = self.gestion_entree.traiter_evenements(events, self.camera)
        self._appliquer_actions(actions)

    def afficher(self, surface):
        etat = self.controleur.get_etat()

        entites_a_portee = etat["entites_a_portee"] if self.gestion_entree.ctrl_est_presse() else []

        surface.fill(self.rendu.couleur_fond)
        self.rendu.dessiner_tout(
            surface,
            self.camera,
            self.controleur.jeu.get_entitees(),
            self.controleur.jeu,
            etat["entite_selectionnee"],
            etat["cases_deplacement"],
            entites_a_portee,
            etat["carte_selectionnee"],
        )

        if etat["partie_terminee"] and etat["joueur_gagnant"]:
            self.rendu.dessiner_ecran_victoire(surface, etat["joueur_gagnant"])

    def update(self, dt):
        _ = dt

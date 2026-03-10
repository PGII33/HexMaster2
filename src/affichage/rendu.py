""" Dessine les éléments à l'écran """
import math
import pygame
from src.affichage.hex_utilitaire import hex_vers_pixel
from src.affichage.sprite_manager import (
    OVERLAY_SELECTION,
    OVERLAY_DEPLACEMENT,
    OVERLAY_COMBAT,
    OVERLAY_DEMOLITION,
    OVERLAY_DEGRADATION,
)
from src.const import (
    CLR_FOND_TERRAIN,
    CLR_FOND_MAIN,
    CLR_CARTE_FOND,
    CLR_CARTE_TEXTE,
    CLR_CARTE_SURBRILLANCE,
    CLR_BTN_FIN_TOUR,
    CLR_BTN_FIN_TOUR_CONTOUR,
    CLR_BTN_FIN_TOUR_TEXTE,
    CLR_EQ_1,
    CLR_EQ_2,
    CLR_EQ_3,
    CLR_EQ_4,
    CLR_EQ_DEF,
    TAILLE_POLICE
)


class Rendu:
    """ Affiche les éléments du jeu à l'écran """

    def __init__(self, sprite_manager):
        # Initialisation de la police
        pygame.font.init()
        self.font = pygame.font.Font(None, TAILLE_POLICE)

        # differentes zones d'affichage
        self.zone_entete = None
        self.zone_terrain = None
        self.zone_info = None
        self.zone_main = None
        self.bouton_fin_tour = None

        # Couleurs et styles
        self.couleur_fond = CLR_FOND_TERRAIN
        self.sprite_manager = sprite_manager

    @staticmethod
    def _overlay_attaque_pour(entite):
        """ Retourne le chemin d'overlay d'attaque selon le type d'entité """
        if entite.est_creature():
            return OVERLAY_COMBAT
        if entite.est_batiment():
            return OVERLAY_DEMOLITION
        return OVERLAY_DEGRADATION

    def _blitter_overlay(self, screen, chemin_overlay, pos_ecran, taille_hex):
        """ Affiche un overlay (sélection, déplacement, attaque) centré sur pos_ecran """
        largeur = math.ceil(taille_hex * 2)
        hauteur = math.ceil(taille_hex * math.sqrt(3))
        overlay = self.sprite_manager.get_overlay(chemin_overlay, largeur, hauteur)
        if overlay:
            rect = overlay.get_rect(center=pos_ecran)
            screen.blit(overlay, rect)

    def dessiner_entete(self, screen, jeu):
        """ Dessine l'en-tête du jeu """
        pygame.draw.rect(screen, (50, 50, 60), self.zone_entete)

        j_act = jeu.get_joueur_actif()
        texte = f"Joueur Actuel: {j_act.get_nom()} | PI : {j_act.get_pi()}"
        texte_surface = self.font.render(texte, True, (255, 255, 255))
        screen.blit(texte_surface, (self.zone_entete.x +
                    10, self.zone_entete.y + 10))

    def dessiner_zones_debug(self, screen):
        """ fonction temporaire, pour le debug des zones d'affichage """
        pygame.draw.rect(screen, (25, 100, 150), self.zone_entete, 2)
        pygame.draw.rect(screen, (100, 100, 255), self.zone_terrain, 2)
        pygame.draw.rect(screen, (255, 100, 100), self.zone_info, 2)
        pygame.draw.rect(screen, (100, 255, 100), self.zone_main, 2)

    def dessiner_bouton_fin_tour(self, screen):
        """ Dessine le bouton fin de tour """
        if self.bouton_fin_tour:
            pygame.draw.rect(screen, CLR_BTN_FIN_TOUR, self.bouton_fin_tour)
            pygame.draw.rect(screen, CLR_BTN_FIN_TOUR_CONTOUR,
                             self.bouton_fin_tour, 3)
            texte = self.font.render(
                "Fin de Tour", True, CLR_BTN_FIN_TOUR_TEXTE)
            texte_rect = texte.get_rect(center=self.bouton_fin_tour.center)
            screen.blit(texte, texte_rect)

    def dessiner_main(self, screen, joueur_actif, carte_selectionnee=None):
        """ Dessine les cartes de la main du joueur actif """
        if not self.zone_main:
            return

        # Fond de la zone
        pygame.draw.rect(screen, CLR_FOND_MAIN, self.zone_main)

        main = joueur_actif.get_main()
        cartes = main.get_cartes()

        if not cartes:
            # Afficher un message si pas de cartes
            texte = self.font.render("Main vide", True, CLR_CARTE_TEXTE)
            texte_rect = texte.get_rect(center=self.zone_main.center)
            screen.blit(texte, texte_rect)
            return

        # Calculer la taille et position de chaque carte
        nb_cartes = len(cartes)
        marge = 10
        espacement = 5

        # Taille de carte proportionnelle à la zone
        hauteur_carte = self.zone_main.height - 2 * marge
        largeur_carte = int(hauteur_carte * 0.7)  # Ratio carte

        # Centrer les cartes
        largeur_totale = nb_cartes * largeur_carte + \
            (nb_cartes - 1) * espacement
        x_depart = self.zone_main.x + \
            (self.zone_main.width - largeur_totale) // 2

        for i, carte in enumerate(cartes):
            x = x_depart + i * (largeur_carte + espacement)
            y = self.zone_main.y + marge

            # Surbrillance si carte sélectionnée
            if carte == carte_selectionnee:
                rect_surbrillance = pygame.Rect(
                    x - 3, y - 3, largeur_carte + 6, hauteur_carte + 6)
                pygame.draw.rect(screen, CLR_CARTE_SURBRILLANCE,
                                 rect_surbrillance, 3)

            # Récupérer le sprite de la carte
            carte_path = carte.get_carte_path()
            sprite_carte = self.sprite_manager.get_sprite_carte(
                carte_path) if carte_path else None

            if sprite_carte:
                # Redimensionner avec lissage pour meilleure qualité
                sprite_redim = pygame.transform.smoothscale(
                    sprite_carte, (largeur_carte, hauteur_carte))
                screen.blit(sprite_redim, (x, y))
            else:
                # Fallback : rectangle avec le nom
                rect_carte = pygame.Rect(x, y, largeur_carte, hauteur_carte)
                couleur = CLR_CARTE_FOND

                pygame.draw.rect(screen, couleur, rect_carte)
                pygame.draw.rect(screen, (255, 255, 255), rect_carte, 2)

                # Nom de la carte
                font_petit = pygame.font.Font(None, 18)
                texte_nom = font_petit.render(carte.get_nom(), True, (0, 0, 0))
                texte_rect = texte_nom.get_rect(
                    center=(x + largeur_carte // 2, y + 20))
                screen.blit(texte_nom, texte_rect)

                # Coût en PI
                texte_cout = font_petit.render(
                    f"Coût: {carte.get_cout()}", True, (0, 0, 0))
                cout_rect = texte_cout.get_rect(
                    center=(x + largeur_carte // 2, y + hauteur_carte - 20))
                screen.blit(texte_cout, cout_rect)

    def get_carte_cliquee(self, pos_pixel, joueur_actif):
        """ Détecte quelle carte a été cliquée dans la main

        Args:
            pos_pixel: Position du clic en pixels
            joueur_actif: Le joueur actif

        Returns:
            L'index de la carte cliquée ou None
        """
        if not self.zone_main:
            return None

        main = joueur_actif.get_main()
        cartes = main.get_cartes()

        if not cartes:
            return None

        # Calculer les positions des cartes (même logique que dessiner_main)
        nb_cartes = len(cartes)
        marge = 10
        espacement = 5
        hauteur_carte = self.zone_main.height - 2 * marge
        largeur_carte = int(hauteur_carte * 0.7)
        largeur_totale = nb_cartes * largeur_carte + \
            (nb_cartes - 1) * espacement
        x_depart = self.zone_main.x + \
            (self.zone_main.width - largeur_totale) // 2

        for i in range(nb_cartes):
            x = x_depart + i * (largeur_carte + espacement)
            y = self.zone_main.y + marge
            rect_carte = pygame.Rect(x, y, largeur_carte, hauteur_carte)

            if rect_carte.collidepoint(pos_pixel):
                return i

        return None

    def calculer_zones(self, largeur_ecran, hauteur_ecran):
        """ Calcule les zones d'affichage """
        self.zone_entete = pygame.Rect(
            0, 0, int(largeur_ecran * 0.8), int(hauteur_ecran * 0.1))
        self.zone_terrain = pygame.Rect(
            0, 0, int(largeur_ecran * 0.8), int(hauteur_ecran * 0.70))
        self.zone_info = pygame.Rect(
            int(largeur_ecran * 0.8), 0, int(largeur_ecran * 0.2), hauteur_ecran)
        self.zone_main = pygame.Rect(
            0, int(hauteur_ecran * 0.70), int(largeur_ecran * 0.8), int(hauteur_ecran * 0.30))

        # Bouton fin de tour en bas à droite
        bouton_w = 150
        bouton_h = 50
        self.bouton_fin_tour = pygame.Rect(
            int(largeur_ecran * 0.8) - bouton_w - 10,
            hauteur_ecran - bouton_h - 10,
            bouton_w,
            bouton_h
        )

    @staticmethod
    def dessiner_hexagone(screen, centre_pixel, taille, couleur, bordure_couleur=(0, 0, 0)):
        """ Dessine un hexagone flat-top """
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = centre_pixel[0] + taille * math.cos(angle)
            y = centre_pixel[1] + taille * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(screen, couleur, points)
        pygame.draw.polygon(screen, bordure_couleur, points, 2)  # Bordure

    def dessiner_entite(self, screen, camera, entite, offset_x, offset_y, entite_selectionnee=None, entites_a_portee=None):
        """ Dessine une entité à l'écran """
        if entites_a_portee is None:
            entites_a_portee = []
        taille_hex = camera.get_taille_hex_actuelle()
        pos_monde = hex_vers_pixel(entite.get_pos(), taille_hex)

        pos_ecran = (
            pos_monde[0] - camera.pos_x + offset_x,
            pos_monde[1] - camera.pos_y + offset_y
        )

        if not self.zone_terrain.collidepoint(pos_ecran):
            return

        # Essayer d'afficher le sprite si disponible (avec couleur d'équipe)
        sprite_path = entite.get_sprite_path()
        sprite = self.sprite_manager.get_sprite_pour_equipe(
            sprite_path, entite.get_equipe()) if sprite_path else None

        if sprite:
            # Redimensionner le sprite selon la taille de l'hexagone
            largeur_sprite = int(taille_hex * 1.5)
            hauteur_sprite = int(taille_hex * 1.5)
            sprite_redim = pygame.transform.scale(
                sprite, (largeur_sprite, hauteur_sprite))

            # Centrer le sprite sur la position
            rect = sprite_redim.get_rect(center=pos_ecran)
            screen.blit(sprite_redim, rect)
        else:
            # Fallback: formes géométriques si pas de sprite
            # Couleur selon l'équipe
            if entite.get_equipe() == 1:
                couleur = CLR_EQ_1
            elif entite.get_equipe() == 2:
                couleur = CLR_EQ_2
            elif entite.get_equipe() == 3:
                couleur = CLR_EQ_3
            elif entite.get_equipe() == 4:
                couleur = CLR_EQ_4
            else:
                couleur = CLR_EQ_DEF

            rayon = taille_hex * 0.4  # Taille de la forme

            # Dessiner selon le type
            if entite.est_creature():
                # Cercle pour les créatures
                pygame.draw.circle(screen, couleur, pos_ecran, int(rayon))
                pygame.draw.circle(screen, (0, 0, 0), pos_ecran,
                                   int(rayon), 2)  # Bordure

            elif entite.est_batiment():
                # Carré pour les bâtiments
                rect = pygame.Rect(0, 0, rayon * 1.5, rayon * 1.5)
                rect.center = pos_ecran
                pygame.draw.rect(screen, couleur, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Bordure

            elif entite.est_sort():
                # Triangle pour les sorts
                hauteur = rayon * 1.2
                points = [
                    (pos_ecran[0], pos_ecran[1] - hauteur),  # Haut
                    (pos_ecran[0] - rayon, pos_ecran[1] +
                     hauteur/2),  # Bas gauche
                    (pos_ecran[0] + rayon, pos_ecran[1] +
                     hauteur/2)   # Bas droit
                ]
                pygame.draw.polygon(screen, couleur, points)
                pygame.draw.polygon(screen, (0, 0, 0), points, 2)  # Bordure

        # Overlay par-dessus le sprite (un seul, par priorité)
        if entite == entite_selectionnee:
            self._blitter_overlay(screen, OVERLAY_SELECTION, pos_ecran, taille_hex)
        elif entites_a_portee and entite in entites_a_portee:
            # Pas d'overlay d'attaque sur la position de l'entité sélectionnée
            if not entite_selectionnee or entite.get_pos() != entite_selectionnee.get_pos():
                self._blitter_overlay(screen, self._overlay_attaque_pour(entite), pos_ecran, taille_hex)

    def dessiner_info_entite(self, screen, entite):
        """ Affiche les informations de l'entité sélectionnée """
        # TODO: Améliorer l'affichage des infos
        # Fond de la zone
        pygame.draw.rect(screen, (60, 60, 70), self.zone_info)

        if not entite:
            return

        # Titre
        texte_titre = self.font.render(
            "Entité sélectionnée", True, (255, 255, 255))
        screen.blit(texte_titre, (self.zone_info.x +
                    10, self.zone_info.y + 10))

        y_offset = 50

        # Nom
        texte = self.font.render(
            f"Nom: {entite.get_nom()}", True, (255, 255, 255))
        screen.blit(texte, (self.zone_info.x + 10,
                    self.zone_info.y + y_offset))
        y_offset += 30

        # get_pv
        texte = self.font.render(
            f"PV: {entite.get_pv()}", True, (255, 255, 255))
        screen.blit(texte, (self.zone_info.x + 10,
                    self.zone_info.y + y_offset))
        y_offset += 30

        # get_control
        if hasattr(entite, 'get_control'):
            texte = self.font.render(
                f"Control: {entite.get_control()}", True, (255, 255, 255))
            screen.blit(texte, (self.zone_info.x + 10,
                        self.zone_info.y + y_offset))
            y_offset += 30

        # get_combat
        if hasattr(entite, 'get_combat'):
            texte = self.font.render(
                f"Combat: {entite.get_combat()}", True, (255, 255, 255))
            screen.blit(texte, (self.zone_info.x + 10,
                        self.zone_info.y + y_offset))
            y_offset += 30

        # get_demolition
        if hasattr(entite, 'get_demolition'):
            texte = self.font.render(
                f"Demolition: {entite.get_demolition()}", True, (255, 255, 255))
            screen.blit(texte, (self.zone_info.x + 10,
                        self.zone_info.y + y_offset))
            y_offset += 30

        # get_degradation
        if hasattr(entite, 'get_degradation'):
            texte = self.font.render(
                f"Degradation: {entite.get_degradation()}", True, (255, 255, 255))
            screen.blit(texte, (self.zone_info.x + 10,
                        self.zone_info.y + y_offset))
            y_offset += 30

        # get_portee
        if hasattr(entite, 'get_portee'):
            texte = self.font.render(
                f"Portée: {entite.get_portee()}", True, (255, 255, 255))
            screen.blit(texte, (self.zone_info.x + 10,
                        self.zone_info.y + y_offset))
            y_offset += 30

    def dessiner_tout(self, screen, camera,
                      entites, jeu, entite_selectionnee=None, cases_deplacement=None, entites_a_portee=None, carte_selectionnee=None):
        """ Dessine tous les éléments du jeu """
        if cases_deplacement is None:
            cases_deplacement = []
        if entites_a_portee is None:
            entites_a_portee = []

        taille_hex = camera.get_taille_hex_actuelle()

        # Calculer l'offset pour centrer dans la zone terrain
        offset_x = self.zone_terrain.x + self.zone_terrain.width // 2
        offset_y = self.zone_terrain.y + self.zone_terrain.height // 2

        # Dessiner les sprites des cases
        for entite in entites:
            if entite.est_case():
                pos_monde = hex_vers_pixel(entite.get_pos(), taille_hex)
                pos_ecran = (
                    pos_monde[0] - camera.pos_x + offset_x,
                    pos_monde[1] - camera.pos_y + offset_y
                )

                # Ne dessiner que si visible dans la zone terrain
                marge = taille_hex * 2
                zone_etendue = self.zone_terrain.inflate(marge * 2, marge * 2)
                if not zone_etendue.collidepoint(pos_ecran):
                    continue

                sprite_path = entite.get_sprite_path()
                if sprite_path:
                    sprite = self.sprite_manager.get_sprite(sprite_path)
                    if sprite:
                        largeur_sprite = math.ceil(taille_hex * 2)
                        hauteur_sprite = math.ceil(taille_hex * math.sqrt(3))
                        sprite_redim = pygame.transform.scale(
                            sprite, (largeur_sprite, hauteur_sprite))
                        rect = sprite_redim.get_rect(center=pos_ecran)
                        screen.blit(sprite_redim, rect)

                # Overlay par-dessus le sprite (un seul par case, par priorité)
                if entite == entite_selectionnee:
                    self._blitter_overlay(screen, OVERLAY_SELECTION, pos_ecran, taille_hex)
                elif entites_a_portee and entite in entites_a_portee:
                    # Pas d'attaque sur la position de l'entité sélectionnée
                    if entite_selectionnee and entite.get_pos() == entite_selectionnee.get_pos():
                        pass
                    else:
                        # Ne pas afficher dégradation si une créature/bâtiment au même endroit est aussi ciblée
                        entite_prioritaire = any(
                            e for e in entites_a_portee
                            if not e.est_case() and e.get_pos() == entite.get_pos()
                        )
                        if not entite_prioritaire:
                            self._blitter_overlay(screen, self._overlay_attaque_pour(entite), pos_ecran, taille_hex)
                elif not entites_a_portee and entite.get_pos() in cases_deplacement:
                    # Pas de déplacement sur la case de l'entité sélectionnée
                    if not entite_selectionnee or entite.get_pos() != entite_selectionnee.get_pos():
                        self._blitter_overlay(screen, OVERLAY_DEPLACEMENT, pos_ecran, taille_hex)

        # Dessiner les créatures, bâtiments et sorts par-dessus les cases
        for entite in entites:
            if not entite.est_case():
                self.dessiner_entite(
                    screen, camera, entite, offset_x, offset_y, entite_selectionnee, entites_a_portee)

        self.dessiner_entete(screen, jeu)
        self.dessiner_info_entite(screen, entite_selectionnee)
        self.dessiner_main(screen, jeu.get_joueur_actif(), carte_selectionnee)
        self.dessiner_bouton_fin_tour(screen)

    @staticmethod
    def dessiner_ecran_victoire(screen, joueur_gagnant):
        """ Affiche l'écran de victoire """
        # TODO: Changer l'affichage, c'est pourquoi je ne m'embête pas à mettre les couleurs dans const.py
        # Overlay semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Texte de victoire
        font_titre = pygame.font.Font(None, 72)
        font_texte = pygame.font.Font(None, 36)

        texte_victoire = font_titre.render("VICTOIRE !", True, (255, 215, 0))
        texte_joueur = font_texte.render(
            f"{joueur_gagnant.get_nom()} a gagné !", True, (255, 255, 255)
        )
        texte_quitter = font_texte.render(
            "Appuyez sur ECHAP pour quitter", True, (200, 200, 200)
        )

        # Centrer les textes
        rect_victoire = texte_victoire.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        rect_joueur = texte_joueur.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        rect_quitter = texte_quitter.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 + 80))

        screen.blit(texte_victoire, rect_victoire)
        screen.blit(texte_joueur, rect_joueur)
        screen.blit(texte_quitter, rect_quitter)

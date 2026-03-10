""" Gère les sprites """

import os
import pygame

OVERLAY_SELECTION = os.path.join("assets", "sprites", "overlay", "selection.png")
OVERLAY_DEPLACEMENT = os.path.join("assets", "sprites", "overlay", "deplacement.png")
OVERLAY_COMBAT = os.path.join("assets", "sprites", "overlay", "combat.png")
OVERLAY_DEMOLITION = os.path.join("assets", "sprites", "overlay", "demolition.png")
OVERLAY_DEGRADATION = os.path.join("assets", "sprites", "overlay", "degradation.png")


class SpriteManager:
    """ Gère la gestion des sprites """

    def __init__(self):
        self.sprites = {}  # chemin -> pygame.Surface
        self.cartes = {}   # chemin -> pygame.Surface
        self._overlay_cache = {} # Overlays redimensionnés en cache, clé: (chemin, largeur, hauteur)
        # Pour ne notifier qu'une fois par sprite manquant
        self.sprite_manquant_notifie = set()
        self.cartes_manquant_notifie = set()

    def charger_sprite(self, chemin):
        """ Charge un sprite depuis un fichier et le met en cache """
        if not chemin:
            return None

        # Vérifier si déjà chargé
        if chemin in self.sprites:
            return self.sprites[chemin]

        # Charger le sprite
        if os.path.exists(chemin):
            try:
                image = pygame.image.load(chemin)
                self.sprites[chemin] = image
                return image
            except pygame.error as e:  # pylint: disable=no-member
                if chemin not in self.sprite_manquant_notifie:
                    print(f"Erreur chargement sprite {chemin}: {e}")
                    self.sprite_manquant_notifie.add(chemin)
                return None
        else:
            if chemin not in self.sprite_manquant_notifie:
                print(f"Sprite introuvable: {chemin}")
                self.sprite_manquant_notifie.add(chemin)
            return None

    def get_sprite(self, chemin):
        """ Récupère le sprite (charge si nécessaire) """
        if not chemin:
            return None
        return self.charger_sprite(chemin)

    def get_sprite_carte(self, chemin):
        """ Récupère le sprite de carte (charge si nécessaire)"""
        return self.charger_sprite(chemin)

    def get_overlay(self, chemin, largeur, hauteur):
        """ Récupère un overlay redimensionné (avec cache)

        Args:
            chemin: Chemin du fichier overlay PNG
            largeur: Largeur souhaitée en pixels
            hauteur: Hauteur souhaitée en pixels

        Returns:
            pygame.Surface redimensionnée avec alpha, ou None
        """
        cle = (chemin, largeur, hauteur)
        if cle in self._overlay_cache:
            return self._overlay_cache[cle]

        sprite = self.charger_sprite(chemin)
        if not sprite:
            return None

        sprite_redim = pygame.transform.scale(
            sprite, (largeur, hauteur))
        self._overlay_cache[cle] = sprite_redim
        return sprite_redim

    def get_sprite_pour_equipe(self, sprite_path, equipe):
        """Récupère le sprite adapté à l'équipe

        Cherche d'abord un sprite spécifique à l'équipe (ex: paysan_team_1.png),
        sinon retourne le sprite de base.

        Returns:
            pygame.Surface ou None si aucun sprite trouvé
        """
        if not sprite_path:
            return None

        # Pour l'équipe neutre (0), utiliser le sprite de base
        if equipe == 0:
            return self.get_sprite(sprite_path)

        # Essayer d'abord avec le sprite d'équipe
        base, ext = os.path.splitext(sprite_path)
        sprite_equipe_path = f"{base}_team_{equipe}{ext}"

        sprite = self.get_sprite(sprite_equipe_path)
        if sprite:
            return sprite

        # Sinon retourner le sprite de base
        return self.get_sprite(sprite_path)

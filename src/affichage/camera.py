"""Gere la logique de la camera."""


class Camera:
    """Camera du jeu avec zoom et taille d'ecran."""

    def __init__(self, largeur_ecran: int, hauteur_ecran: int, taille_hex_base: int = 50):
        self.pos_x = 0
        self.pos_y = 0
        self.zoom = 1.0
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.taille_hex_base = taille_hex_base

        # Limites de zoom
        self.zoom_min = 0.5
        self.zoom_max = 3.0

    def get_taille_hex_actuelle(self) -> float:
        """Taille d'un hex en pixels selon le zoom."""
        return self.taille_hex_base * self.zoom

    def set_taille_ecran(self, largeur: int, hauteur: int) -> None:
        """Met a jour la taille de l'ecran."""
        self.largeur_ecran = largeur
        self.hauteur_ecran = hauteur

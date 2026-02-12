""" Gère la logique de la caméra"""
class Camera:
    """ La camera du jeu"""
    def __init__(self, largeur_ecran, hauteur_ecran, taille_hex_base=50):
        self.pos_x = 0
        self.pos_y = 0
        self.zoom = 1.0
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.taille_hex_base = taille_hex_base

        # Limites de zoom
        self.zoom_min = 0.5
        self.zoom_max = 3.0

    def get_taille_hex_actuelle(self):
        """Taille d'un hex en pixels selon le zoom"""
        return self.taille_hex_base * self.zoom

    def set_taille_ecran(self, largeur, hauteur):
        """ Met à jour la taille de l'écran """
        self.largeur_ecran = largeur
        self.hauteur_ecran = hauteur

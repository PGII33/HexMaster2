""" Fichier pour le bouton presque hexagonal du menu principal """

import pygame


class BoutonHex:
    """ Classe pour le bouton presque hexagonal du menu principal"""
    def __init__(self, x:int, y:int, width:int, height:int,
                 text:str, font:pygame.font.Font, action: str|None = None,
                 couleur_base:tuple[int, int, int] = (52, 225, 255),
                 couleur_hover:tuple[int, int, int] = (90, 235, 255),
                 couleur_pressed:tuple[int, int, int] = (30, 200, 255),
                 couleur_texte:tuple[int, int, int] = (0, 0, 0),
                 couleur_bordure:tuple[int, int, int] = (0, 0, 0),
                 epaisseur_bordure: int = 2,
                 hover_scale: float = 1.03,
                 pressed_scale: float = 0.95,
                 click_anim_ms:int = 100,
                 chamfer_ratio:float = 0.22 #chamfer = ratio de la largeur du bouton pour les coins biseautés
                 ) -> None:
        self._base_rect = pygame.Rect(x, y, width, height)
        self._rect = self._base_rect.copy()

        self._text = text
        self._font = font
        self._action = action

        self._couleur_base = couleur_base
        self._couleur_hover = couleur_hover
        self._couleur_pressed = couleur_pressed
        self._couleur_texte = couleur_texte
        self._couleur_bordure = couleur_bordure
        self._epaisseur_bordure = epaisseur_bordure

        self._hover: bool = False
        self._pressed: bool = False

        self._scale: float = 1.0
        self._target_scale: float = 1.0
        self._hover_scale = hover_scale
        self._pressed_scale = pressed_scale

        self._click_anim_ms = click_anim_ms
        self._click_timer_ms: int = 0

        self._chamfer_ratio = max(0.05, min(chamfer_ratio, 0.45))

        self._polygon: list[tuple[float, float]] = []
        self._rebuild_polygon()
    
    def get_action(self) -> str|None:
        """ Retourner l'action associée au bouton"""
        return self._action
    
    def set_action(self, action:str|None):
        """ Définir l'action associée au bouton"""
        self._action = action

    def set_text(self, text:str):
        """ Définir le texte du bouton"""
        self._text = text

    def handle_event(self, event:pygame.event.Event) ->bool:
        """ Traite un evenement pygame. Retourne True si le bouton est active."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.collidepoint(event.pos):
                self._pressed = True
                self._target_scale = self._pressed_scale
                self._click_timer_ms = self._click_anim_ms
                return False
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            a_ete_presse = self._pressed
            self._pressed = False
            if a_ete_presse and self.collidepoint(event.pos):
                self._target_scale = self._hover_scale
                return True
        
        return False
    
    def update(self, dt:int, mouse_pos:tuple[int, int]):
        """ Met à jour l'état visuel (hover + animation)."""
        self._hover = self.collidepoint(mouse_pos)

        if self._click_timer_ms > 0:
            self._click_timer_ms -= dt
            if self._click_timer_ms <= 0:
                self._target_scale = self._hover_scale if self._hover else 1.0
        
        else:
            if self._pressed:
                self._target_scale = self._pressed_scale
            elif self._hover:
                self._target_scale = self._hover_scale
            else:
                self._target_scale = 1.0

        vitesse = min(1.0, 0.02 * dt)
        self._scale += (self._target_scale - self._scale) * vitesse
        self._update_rect_from_scale()
    
    def afficher(self, surface: pygame.Surface)-> None:
        """ Dessine le bouton """
        if self._pressed or self._click_timer_ms > 0:
            fill = self._couleur_pressed
        elif self._hover:
            fill = self._couleur_hover
        else:
            fill = self._couleur_base
        
        pygame.draw.polygon(surface, fill, self._polygon)
        if self._epaisseur_bordure > 0:
            pygame.draw.polygon(surface, self._couleur_bordure, self._polygon, self._epaisseur_bordure)

        texte_surface = self._font.render(self._text, True, self._couleur_texte)
        texte_rect = texte_surface.get_rect(center=self._rect.center)
        surface.blit(texte_surface, texte_rect)

    def collidepoint(self, point:tuple[int, int]) -> bool:
        """ Test point dans polygone (ray-casting)"""
        px, py = point

        if not self._rect.collidepoint(point):
            return False
        
        dedans = False
        j = len(self._polygon) - 1
        for i in range(len(self._polygon)):
            xi, yi = self._polygon[i]
            xj, yj = self._polygon[j]
            
            intersection = ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi)
            if intersection:
                dedans = not dedans
            j = i
        return dedans
    
    def _update_rect_from_scale(self):
        """ Met à jour le rectangle du bouton en fonction de l'échelle actuelle"""
        center = self._base_rect.center
        self._rect.width = self._base_rect.width * self._scale
        self._rect.height = self._base_rect.height * self._scale
        self._rect.center = center
        self._rebuild_polygon()

    def _rebuild_polygon(self):
        """ Construit le polygone 6 face flat-top etire """
        cx, cy = self._rect.center
        w: float = float(self._rect.width)
        h: float = float(self._rect.height)

        c = w * self._chamfer_ratio
        c = max(8.0, min(c, w*0.45))

        gauche: float = cx - w/2.0
        droite: float = cx + w/2.0
        haut: float = cy - h/2.0
        bas: float = cy + h/2.0

        self._polygon = [
            (gauche + c, haut),  # coin haut gauche
            (droite - c, haut),  # coin haut droit
            (droite, cy),        # milieu droit
            (droite - c, bas),   # coin bas droit
            (gauche + c, bas),   # coin bas gauche
            (gauche, cy)         # milieu gauche
        ]
    
""" Slider pour l'UI """

import pygame

class Slider:
    """ Classe pour un slider dans l'interface utilisateur"""
    def __init__(self, x:int, y:int, width:int, height:int, min_value:float=0.0, max_value:float=1.0, initial_value:float=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value: float = min_value
        self.max_value: float = max_value
        self.value: float = initial_value

        self.dragging = False
        self.thumb_radius = 10

    def get_value(self) -> float:
        """ Retourner la valeur actuelle du slider"""
        return self.value

    def _value_to_t(self):
        """ Convertir la valeur actuelle en un t normalisé entre 0 et 1 pour le positionnement du thumb"""
        return (self.value - self.min_value) / (self.max_value - self.min_value)

    def _t_to_value(self, t):
        """" Convertir un t normalisé entre 0 et 1 en une valeur dans l'intervalle [min_value, max_value]"""
        t = max(0, min(1, t))
        return self.min_value + t * (self.max_value - self.min_value)

    def _thumb_center(self):
        t = self._value_to_t()
        x = int(self.rect.left + t * self.rect.width)
        y = self.rect.centery
        return (x, y)
    
    def handle_event(self, event):
        changed = False
        thumb = self._thumb_center()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Vector2(event.pos).distance_to(thumb) <= self.thumb_radius + 2 or self.rect.collidepoint(event.pos):
                self.dragging = True
                changed = self._update_from_mouse_x(event.pos[0])

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            changed = self._update_from_mouse_x(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        return changed
    
    def _update_from_mouse_x(self, mouse_x):
        old = self.value
        t = (mouse_x - self.rect.left) / self.rect.width
        self.value = self._t_to_value(t)
        return abs(self.value - old) > 1e-6
    

    def afficher(self, surface):
        # track
        pygame.draw.rect(surface, (90, 90, 90), self.rect, border_radius=4)

        # filled
        filled_width = int(self._value_to_t() * self.rect.width)
        filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_width, self.rect.height)
        pygame.draw.rect(surface, (52, 225, 255), filled_rect, border_radius=4)

        # thumb
        pygame.draw.circle(surface, (240, 240, 240), self._thumb_center(), self.thumb_radius)
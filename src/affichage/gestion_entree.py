""" Conversion des entrées utilisateur en actions de jeu """
# pylint: disable=no-member

import pygame


class GestionEntree:
    """ Gestion des entrées utilisateur """

    def __init__(self):
        self.clic_droit_enfonce = False
        self.derniere_pos_souris = None
        self.entite_selectionnee = None
        self.cases_deplacement = []
        self.entites_a_portee = []

    def traiter_evenements(self, events, camera):
        """ Gère les entrees et modifie la caméra """
        actions = []  # actions à retourner au jeu
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # Permet de se déplacer sur la carte, ou d'annuler la sélection d'une carte ou d'une créature
                self.clic_droit_enfonce = True
                self.derniere_pos_souris = pygame.mouse.get_pos()
                actions.append({
                    "type": "deselection"
                })

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                self.clic_droit_enfonce = False

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Zoom
                    camera.zoom = min(camera.zoom * 1.1, camera.zoom_max)
                elif event.y < 0:  # Dezoom
                    camera.zoom = max(camera.zoom / 1.1, camera.zoom_min)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Détecter si Shift ou Ctrl est enfoncé
                mods = pygame.key.get_mods()
                shift_enfonce = mods & pygame.KMOD_SHIFT
                ctrl_enfonce = mods & (
                    pygame.KMOD_CTRL | pygame.KMOD_LCTRL | pygame.KMOD_RCTRL)

                actions.append({
                    "type": "selection",
                    "pos_pixel": event.pos,
                    "shift": bool(shift_enfonce),
                    "ctrl": bool(ctrl_enfonce)
                })

        if self.clic_droit_enfonce:
            pos_actuelle = pygame.mouse.get_pos()
            if self.derniere_pos_souris:
                dx = pos_actuelle[0] - self.derniere_pos_souris[0]
                dy = pos_actuelle[1] - self.derniere_pos_souris[1]
                camera.pos_x -= dx
                camera.pos_y -= dy
            self.derniere_pos_souris = pos_actuelle

        return actions

    @staticmethod
    def ctrl_est_presse():
        """ Vérifie si Ctrl est actuellement pressé """
        mods = pygame.key.get_mods()
        return bool(mods & (pygame.KMOD_CTRL | pygame.KMOD_LCTRL | pygame.KMOD_RCTRL))

    @staticmethod
    def shift_est_presse():
        """ Vérifie si Shift est actuellement pressé """
        mods = pygame.key.get_mods()
        return bool(mods & (pygame.KMOD_SHIFT | pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT))

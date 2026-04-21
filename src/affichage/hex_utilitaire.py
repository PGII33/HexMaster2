""" Fichier de gestion de coordonnées hex vers pixels """
import math

def hex_vers_pixel(pos_hex:tuple[int, int], taille_hex:int) -> tuple[int, int]:
    """ Convertit des coordonnées hexagonales en coordonnées pixels """
    q, r = pos_hex
    x = taille_hex * (3/2 * q)
    y = taille_hex * (math.sqrt(3) * (r + q / 2))
    return int(x), int(y)

def pixel_vers_hex(pos_pixel:tuple[int, int], taille_hex:int):
    """ Convertit des coordonnées pixels en coordonnées hexagonales """
    x, y = pos_pixel
    q = (2/3 * x) / taille_hex
    r = (-1/3 * x + math.sqrt(3)/3 * y) / taille_hex
    return int(round(q)), int(round(r))

def ecran_vers_hex(pos_pixel: tuple[int, int], zone_terrain, camera) -> tuple[int, int]:
    """ Convertit une position écran (pixel) en coordonnées hex du plateau en tenant compte de la zone de rendu et du décalage caméra. """
    offset_x = zone_terrain.x + zone_terrain.width // 2
    offset_y = zone_terrain.y + zone_terrain.height // 2

    pos_monde = (
        pos_pixel[0] - offset_x + camera.pos_x,
        pos_pixel[1] - offset_y + camera.pos_y,
    )
    taille_hex = camera.get_taille_hex_actuelle()
    return pixel_vers_hex(pos_monde, taille_hex)

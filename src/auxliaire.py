""" Fichier de fonctions auxiliaires """

def distance_hex(a:tuple[int, int], b:tuple[int, int]) -> int:
    """ Calcule la distance entre deux hexagones """
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return (abs(dx) + abs(dy) + abs(dx + dy)) // 2

def est_a_distance_hex(a:tuple[int, int], b:tuple[int, int], dist:int) -> bool:
    """ Retourne vrai si deux hexagones sont a une distance donnee """
    return distance_hex(a, b) == dist

def est_a_portee_hex(a:tuple[int, int], b:tuple[int, int], portee:int) -> bool:
    """ Retourne vrai si deux hexagones sont a une portee donnee """
    return distance_hex(a, b) <= portee

def a_distance_hex(a:tuple[int, int], dist:int) -> list[tuple[int, int]]:
    """ Renvoie les hexagones a distance donnee """
    result = []
    for dx in range(-dist, dist + 1):
        for dy in range(max(-dist, -dx - dist), min(dist, -dx + dist) + 1):
            if distance_hex(a, (a[0] + dx, a[1] + dy)) == dist:
                result.append((a[0] + dx, a[1] + dy))
    return result

def a_portee_hex(a:tuple[int, int], portee:int) -> list[tuple[int, int]]:
    """ Renvoie les hexagones a portee donnee """
    result = []
    for d in range(portee + 1):
        result.extend(a_distance_hex(a, d))
    return result

def adjacents_hex(pos:tuple[int, int]) -> list[tuple[int, int]]:
    """ Retourne les positions adjacentes d'un hexagone """
    return a_distance_hex(pos, 1)

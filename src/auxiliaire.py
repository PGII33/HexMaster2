""" Fichier de fonctions auxiliaires """

from collections import deque


def distance_hex(a: tuple[int, int], b: tuple[int, int]) -> int:
    """ Calcule la distance entre deux hexagones """
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return (abs(dx) + abs(dy) + abs(dx + dy)) // 2


def est_a_distance_hex(a: tuple[int, int], b: tuple[int, int], dist: int) -> bool:
    """ Retourne vrai si deux hexagones sont a une distance donnee """
    return distance_hex(a, b) == dist


def est_a_portee_hex(a: tuple[int, int], b: tuple[int, int], portee: int) -> bool:
    """ Retourne vrai si deux hexagones sont a une portee donnee """
    return distance_hex(a, b) <= portee


def a_distance_hex(a: tuple[int, int], dist: int) -> list[tuple[int, int]]:
    """ Renvoie les hexagones a distance donnee """
    result = []
    for dx in range(-dist, dist + 1):
        for dy in range(max(-dist, -dx - dist), min(dist, -dx + dist) + 1):
            if distance_hex(a, (a[0] + dx, a[1] + dy)) == dist:
                result.append((a[0] + dx, a[1] + dy))
    return result


def a_portee_hex(a: tuple[int, int], portee: int) -> list[tuple[int, int]]:
    """ Renvoie les hexagones a portee donnee """
    result = []
    for d in range(portee + 1):
        result.extend(a_distance_hex(a, d))
    return result


def adjacents_hex(pos: tuple[int, int]) -> list[tuple[int, int]]:
    """ Retourne les positions adjacentes d'un hexagone """
    return a_distance_hex(pos, 1)


def _infos_deplacement(terrain, creature) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """Construit les ensembles utiles pour le calcul de déplacement."""
    positions_cases = set()
    positions_bloquees = set()

    for entite in terrain.get_entites():
        position = entite.get_pos()
        if entite.est_case():
            positions_cases.add(position)
        elif (entite.est_creature() or entite.est_batiment()) and entite != creature:
            positions_bloquees.add(position)

    return positions_cases, positions_bloquees


def _distances_deplacement(creature, terrain) -> dict[tuple[int, int], int]:
    """Calcule le coût minimal vers chaque case atteignable en tenant compte des obstacles."""
    mouvement_max = creature.get_mouv()
    position_origine = creature.get_pos()
    positions_cases, positions_bloquees = _infos_deplacement(terrain, creature)

    if position_origine not in positions_cases:
        return {}

    distances = {position_origine: 0}
    a_visiter = deque([position_origine])

    while a_visiter:
        position = a_visiter.popleft()
        distance = distances[position]

        if distance >= mouvement_max:
            continue

        for voisine in adjacents_hex(position):
            if voisine in distances:
                continue
            if voisine not in positions_cases or voisine in positions_bloquees:
                continue

            distances[voisine] = distance + 1
            a_visiter.append(voisine)

    return distances


def get_cases_deplacement(creature, terrain) -> list:
    """ Retourne les cases où la créature peut se déplacer

    Args:
        creature: Instance de Creature
        terrain: Instance de Terrain

    Returns:
        Liste des positions (q, r) libres et accessibles
    """
    return list(_distances_deplacement(creature, terrain).keys())


def get_cout_deplacement(creature, terrain, destination: tuple[int, int]) -> int | None:
    """Retourne le coût minimal pour atteindre une destination, ou None si inaccessible."""
    return _distances_deplacement(creature, terrain).get(destination)


def get_entites_a_portee(creature, terrain) -> list:
    """ Retourne les entités à portée d'attaque de la créature

    Args:
        creature: Instance de Creature/Batiment
        terrain: Instance de Terrain

    Returns:
        Liste des entités attaquables
    """
    portee_attaque = creature.get_portee()
    pos_origine = creature.get_pos()

    # Si portée 0, uniquement la même case
    if portee_attaque == 0:
        positions_a_portee = [pos_origine]
    else:
        # Toutes les positions dans le rayon d'attaque
        positions_a_portee = a_portee_hex(pos_origine, portee_attaque)

    # Récupérer toutes les entités à ces positions
    entites_a_portee = []
    for entite in terrain.get_entites():
        if entite.get_pos() in positions_a_portee and entite != creature:
            entites_a_portee.append(entite)

    return entites_a_portee
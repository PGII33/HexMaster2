""" Fichier de fonctions auxiliaires """


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


def get_cases_deplacement(creature, terrain) -> list:
    """ Retourne les cases où la créature peut se déplacer

    Args:
        creature: Instance de Creature
        terrain: Instance de Terrain

    Returns:
        Liste des positions (q, r) libres et accessibles
    """
    portee_mouvement = creature.get_mouv()
    pos_origine = creature.get_pos()

    # Toutes les positions théoriques dans le rayon de mouvement
    positions_theoriques = a_portee_hex(pos_origine, portee_mouvement)

    # Filtrer pour ne garder que les cases valides
    cases_libres = []
    for pos in positions_theoriques:
        case_existe = False
        occupe = False

        for entite in terrain.get_entites():
            if entite.get_pos() == pos:
                # Vérifier qu'il y a une case à cette position
                if entite.est_case():
                    case_existe = True
                # Vérifier si occupée par créature ou bâtiment
                if (entite.est_creature() or entite.est_batiment()) and entite != creature:
                    occupe = True

        # Ajouter seulement si case existe ET n'est pas occupée
        if case_existe and not occupe:
            cases_libres.append(pos)

    return cases_libres


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
""" Fichier de gestion des effets """

class Effet:
    """ Les effets """
    def __init__(self):
        pass

    def damage_entite_sur_case(self, origine, toutes_entitees):
        """ Effet qui inflige des degats a la cible """
        for cible in toutes_entitees:
            if cible.get_pos() == origine.get_pos() and cible.est_creature():
                cible.set_pv(cible.get_pv() - 3)

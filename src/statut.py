""" Fichier de gestion des statuts actifs """

from src.phase import PhaseTour


class StatutActif:
    """ Représente un statut persistant appliqué à une entité """

    def __init__(self, nom: str, duree: int, phase: PhaseTour = PhaseTour.FIN_TOUR,
                 modificateurs: dict[str, int] = None, nom_effet: str = None, est_buff:bool = False):
        """ Initialise un statut actif, par défaut, il est considéré comme debuff"""
        self.nom = nom
        self.duree_restante = duree
        self.phase = phase
        self.modificateurs = dict(modificateurs) if modificateurs is not None else {}
        self.est_buff = est_buff
        self.nom_effet = nom_effet

    def get_nom(self):
        """ Retourne le nom du statut """
        return self.nom

    def get_duree_restante(self):
        """ Retourne le nombre de tours restants """
        return self.duree_restante

    def est_buff(self):
        """ Retourne vrai si le statut est un buff, faux si c'est un debuff """
        return self.est_buff

    def est_debuff(self):
        """ Retourne vrai si le statut est un debuff, faux si c'est un buff """
        return not self.est_buff

    def set_duree_restante(self, duree: int):
        """ Modifie la durée restante du statut """
        self.duree_restante = duree

    def rafraichir(self, duree: int = None, modificateurs: dict[str, int] = None,
                   phase: PhaseTour = None, nom_effet: str = None):
        """ Rafraîchit les données du statut lors d'une réapplication """
        if duree is not None:
            self.duree_restante = duree
        if modificateurs is not None:
            self.modificateurs = dict(modificateurs)
        if phase is not None:
            self.phase = phase
        if nom_effet is not None:
            self.nom_effet = nom_effet

    def decrementer(self):
        """ Décrémente la durée d'un tour si elle est positive """
        if self.duree_restante > 0:
            self.duree_restante -= 1

    def est_expire(self):
        """ Retourne vrai si le statut est expiré """
        return self.duree_restante == 0

    def get_phase(self):
        """ Retourne la phase d'activation du statut """
        return self.phase

    def get_nom_effet(self):
        """ Retourne le nom de l'effet à résoudre pour ce statut """
        if self.nom_effet is not None:
            return self.nom_effet
        return self.nom.lower().replace(" ", "_")

    def get_modificateur(self, statistique: str):
        """ Retourne le modificateur d'une statistique donnée """
        return self.modificateurs.get(statistique, 0)

    def get_modificateurs(self):
        """ Retourne tous les modificateurs du statut """
        return dict(self.modificateurs)

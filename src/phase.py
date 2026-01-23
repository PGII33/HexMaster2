""" Fichier de creation de phases """
from enum import IntEnum, auto

class PhaseTour(IntEnum):
    """ Enum des phases d'un tour """
    DEBUT_TOUR = auto()
    FIN_TOUR = auto()
    AVANT_ATTAQUE = auto()
    APRES_ATTAQUE = auto()
    APPARITION = auto()
    MORT = auto()
    ACTIF = auto()

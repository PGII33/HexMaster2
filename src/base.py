""" Fichier de gestion de base """

from src.competence import Competence

class Base:
    """ Classe de base """
    def __init__(self, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, comp:list[Competence]=None, sprite_path:str=None,
                 carte_path:str=None):
        """ Initialise la base """
        self.nom = nom
        self.pos = pos
        self.cout = cout
        self.equipe = equipe
        self.comp = comp if comp is not None else []
        self.sprite_path = sprite_path
        self.carte_path = carte_path

    def get_nom(self):
        """ Retourne le nom """
        return self.nom

    def set_nom(self, nom:str):
        """ Modifie le nom """
        self.nom = nom

    def get_pos(self):
        """ Retourne la position axiale """
        return self.pos

    def set_pos(self, pos:tuple[int, int]):
        """ Modifie la position axiale """
        self.pos = pos

    def get_cout(self):
        """ Retourne le cout """
        return self.cout

    def set_cout(self, cout:int):
        """ Modifie le cout """
        self.cout = cout

    def get_sprite_path(self):
        """ Retourne le chemin du sprite """
        return self.sprite_path

    def get_carte_path(self):
        """ Retourne le chemin de la carte """
        return self.carte_path

    def get_equipe(self):
        """ Retourne l'equipe """
        return self.equipe

    def set_equipe(self, equipe:int):
        """ Modifie l'equipe """
        self.equipe = equipe

    def get_comp(self):
        """ Retourne les competences """
        return self.comp

    def set_comp(self, comp:list[Competence]):
        """ Modifie les competences """
        self.comp = comp

    def ajouter_competence(self, comp:Competence):
        """ Ajoute une competence """
        self.comp.append(comp)

    def retirer_competence(self, comp:Competence):
        """ Retire une competence """
        if comp in self.comp:
            self.comp.remove(comp)

# Getters particuliers

    def est_creature(self):
        """ Retourne vrai si l'entite est une creature """
        return False

    def est_batiment(self):
        """ Retourne vrai si l'entite est un batiment """
        return False

    def est_sort(self):
        """ Retourne vrai si l'entite est un sort """
        return False

    def est_case(self):
        """ Retourne vrai si l'entite est une case """
        return False

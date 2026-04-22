""" Fichier de gestion de base """

from __future__ import annotations
from src.competences import Competence

class Base:
    """ Classe de base """
    def __init__(self, nom:str, pos:tuple[int, int], cout:int,
                 equipe:int, comp:list[Competence]=None, tags:list[Tag]=None, sprite_path:str=None,
                 carte_path:str=None):
        """ Initialise la base """
        self.nom = nom
        self.pos = pos
        self.cout = cout
        self.equipe = equipe
        self.comp = comp if comp is not None else []
        self.statuts_actif = []
        self.tags = tags if tags is not None else []
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
        """ Retourne l'équipe """
        return self.equipe

    def set_equipe(self, equipe:int):
        """ Modifie l'équipe """
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

    def get_tags(self):
        """ Retourne les tags """
        return self.tags

    def set_tags(self, tags:list[Tag]):
        """ Modifie les tags """
        self.tags = tags
    
    def ajouter_tag(self, tag:Tag):
        """ Ajoute un tag """
        self.tags.append(tag)
    
    def retirer_tag(self, tag:Tag):
        """ Retire un tag """
        if tag in self.tags:
            self.tags.remove(tag)

    def get_statuts(self):
        """ Retourne les statuts actifs de l'entité """
        return self.statuts_actif

    def get_statut(self, nom: str):
        """ Retourne le statut actif portant un nom donné """
        nom_normalise = nom.lower()
        for statut in self.statuts_actif:
            if statut.get_nom().lower() == nom_normalise:
                return statut
        return None

    def ajouter_statut(self, statut):
        """ Ajoute un statut actif ou rafraîchit un statut existant """
        statut_existant = self.get_statut(statut.get_nom())
        if statut_existant is not None:
            statut_existant.rafraichir(
                duree=statut.get_duree_restante(),
                modificateurs=statut.get_modificateurs(),
                phase=statut.get_phase(),
                nom_effet=statut.get_nom_effet()
            )
        else:
            self.statuts_actif.append(statut)

        self.recalculer_stats_depuis_statuts()

    def retirer_statut(self, nom: str):
        """ Retire un statut actif par son nom """
        statut = self.get_statut(nom)
        if statut is not None:
            self.statuts_actif.remove(statut)
            self.recalculer_stats_depuis_statuts()

    def appliquer_statuts(self, phase, toutes_entitees, joueurs=None):
        """ Déclenche les effets des statuts correspondant à une phase """
        from src.effets import Effet  # pylint: disable=import-outside-toplevel

        for statut in list(self.statuts_actif):
            if statut.get_phase() != phase:
                continue

            nom_effet = statut.get_nom_effet()
            if nom_effet is None or not hasattr(Effet, nom_effet):
                continue

            methode = getattr(Effet, nom_effet)
            if joueurs is not None:
                methode(self, toutes_entitees, None, joueurs)
            else:
                methode(self, toutes_entitees)

    def decrementer_statuts(self, phase):
        """ Décrémente et purge les statuts d'une phase donnée """
        statuts_expire = []
        for statut in self.statuts_actif:
            if statut.get_phase() != phase:
                continue
            statut.decrementer()
            if statut.est_expire():
                statuts_expire.append(statut)

        for statut in statuts_expire:
            self.statuts_actif.remove(statut)

        if statuts_expire:
            self.recalculer_stats_depuis_statuts()

    def get_modificateur_statut(self, statistique: str):
        """ Somme les modificateurs d'une statistique sur tous les statuts actifs """
        return sum(statut.get_modificateur(statistique) for statut in self.statuts_actif)

    def recalculer_stats_depuis_statuts(self):
        """ Point d'extension pour recalculer les stats dérivées """

# Getters particuliers

    def est_creature(self):
        """ Retourne vrai si l'entité est une creature """
        return False

    def est_batiment(self):
        """ Retourne vrai si l'entité est un bâtiment """
        return False

    def est_sort(self):
        """ Retourne vrai si l'entité est un sort """
        return False

    def est_case(self):
        """ Retourne vrai si l'entité est une case """
        return False

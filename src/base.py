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
        self.tags_actifs = []
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
        """ Retourne les tags actifs de l'entité """
        return self.tags_actifs

    def get_tag(self, nom: str):
        """ Retourne le tag actif portant un nom donné """
        nom_normalise = nom.lower()
        for tag in self.tags_actifs:
            if tag.get_nom().lower() == nom_normalise:
                return tag
        return None

    def ajouter_tag(self, tag):
        """ Ajoute un tag actif ou rafraîchit un tag existant """
        tag_existant = self.get_tag(tag.get_nom())
        if tag_existant is not None:
            tag_existant.rafraichir(
                duree=tag.get_duree_restante(),
                modificateurs=tag.get_modificateurs(),
                phase=tag.get_phase(),
                nom_effet=tag.get_nom_effet()
            )
        else:
            self.tags_actifs.append(tag)

        self.recalculer_stats_depuis_tags()

    def retirer_tag(self, nom: str):
        """ Retire un tag actif par son nom """
        tag = self.get_tag(nom)
        if tag is not None:
            self.tags_actifs.remove(tag)
            self.recalculer_stats_depuis_tags()

    def resoudre_tags(self, phase, toutes_entitees, joueurs=None):
        """ Déclenche les effets des tags correspondant à une phase """
        from src.effet import Effet  # pylint: disable=import-outside-toplevel

        for tag in list(self.tags_actifs):
            if tag.get_phase() != phase:
                continue

            nom_effet = tag.get_nom_effet()
            if nom_effet is None or not hasattr(Effet, nom_effet):
                continue

            methode = getattr(Effet, nom_effet)
            if joueurs is not None:
                methode(self, toutes_entitees, None, joueurs)
            else:
                methode(self, toutes_entitees)

    def decrementer_tags(self, phase):
        """ Décrémente et purge les tags d'une phase donnée """
        tags_expire = []
        for tag in self.tags_actifs:
            if tag.get_phase() != phase:
                continue
            tag.decrementer()
            if tag.est_expire():
                tags_expire.append(tag)

        for tag in tags_expire:
            self.tags_actifs.remove(tag)

        if tags_expire:
            self.recalculer_stats_depuis_tags()

    def get_modificateur_tag(self, statistique: str):
        """ Somme les modificateurs d'une statistique sur tous les tags actifs """
        return sum(tag.get_modificateur(statistique) for tag in self.tags_actifs)

    def recalculer_stats_depuis_tags(self):
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

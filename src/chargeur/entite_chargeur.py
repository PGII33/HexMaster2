""" Charge les entites depuis des fichiers JSON """
import json
import os
from src.creature import Creature
from src.batiment import Batiment
from src.case import Case
from src.sort import Sort
from src.competences import Competence
from src.phase import PhaseTour
from src.tag import Tag
from src.chargeur.effet_chargeur import EffetChargeur
from src.chargeur.statut_chargeur import StatutChargeur
from src.effets import Effet
from src.statut import StatutActif


class EntiteChargeur:
    """ Chargeur d'entites depuis des fichiers JSON """

    def __init__(self, chemin_data="data/entites", chemin_mods="mods", chemin_effets_data="data/effets", chemin_statuts_data="data/statuts"):
        self.chemin_data = chemin_data
        self.chemin_mods = chemin_mods
        self.entites_chargees = {}
        self.mods_actifs = self.charger_mods_actifs()
        self.effet_chargeur = EffetChargeur(chemin_data=chemin_effets_data, chemin_mods=chemin_mods)
        self.effet_chargeur.charger_tous_les_effets()
        self.statut_chargeur = StatutChargeur(chemin_data=chemin_statuts_data, chemin_mods=chemin_mods)
        self.statut_chargeur.charger_tous_les_statuts()
        StatutActif.enregistrer_statuts_custom(self.statut_chargeur.statuts_chargees)
        Effet.enregistrer_effets_custom(self.effet_chargeur.effets_chargees)

    def charger_mods_actifs(self):
        """Retourne les dossiers de premier niveau présents dans le dossier des mods."""
        if not os.path.exists(self.chemin_mods):
            return []

        mods = []
        for entree in os.scandir(self.chemin_mods):
            if entree.is_dir():
                mods.append(entree.name)

        return mods

    def charger_toutes_les_entites(self):
        """Charge toutes les entités depuis data/ et mods/"""
        self.charger_depuis_dossier(self.chemin_data)

        for mod in self.mods_actifs:
            print(f"Chargement des entités du mod : {mod}")
            self.charger_depuis_dossier(os.path.join(self.chemin_mods, mod, "data", "entites"))

    def charger_depuis_dossier(self, chemin):
        """Parcourt récursivement un dossier et charge tous les fichiers JSON"""
        if not os.path.exists(chemin):
            return

        for root, _, files in os.walk(chemin):
            for fichier in files:
                if fichier.endswith('.json'):
                    chemin_complet = os.path.join(root, fichier)
                    self.charger_entite(chemin_complet)

    def charger_entite(self, fichier_json):
        """Charge une entité depuis un fichier JSON"""
        with open(fichier_json, 'r', encoding='utf-8') as f:
            definition = json.load(f)

        id_entite = definition.get("id")
        if id_entite:
            self.entites_chargees[id_entite] = definition

    def creer_instance(self, id_entite, pos, equipe):
        """Crée une instance d'entité à partir de sa définition"""
        if id_entite not in self.entites_chargees:
            raise ValueError(
                f"Entité '{id_entite}' non trouvée dans les définitions chargées")

        definition = self.entites_chargees[id_entite]

        if definition["type"] == "creature":
            return self.creer_creature(definition, pos, equipe)
        elif definition["type"] == "batiment":
            return self.creer_batiment(definition, pos, equipe)
        elif definition["type"] == "case":
            return self.creer_case(definition, pos, equipe)
        elif definition["type"] == "sort":
            return self.creer_sort(definition, pos, equipe)
        else:
            raise ValueError(f"Type d'entité inconnu: {definition['type']}")

    def charger_competences(self, definition):
        """ Charge les compétences depuis la définition JSON

        Args:
            definition: Dictionnaire contenant la définition de l'entité

        Returns:
            Liste de compétences ou liste vide
        """
        competences = []

        if "competences" not in definition:
            return competences

        for comp_def in definition["competences"]:
            nom_comp = comp_def.get("nom")
            phase_str = comp_def.get("phase")

            if phase_str is None and nom_comp is not None:
                phase_effet = self.effet_chargeur.get_phase_effet(nom_comp)
                if phase_effet is not None:
                    phase = phase_effet
                else:
                    phase = PhaseTour.FIN_TOUR
            else:
                phase = getattr(PhaseTour, phase_str, PhaseTour.FIN_TOUR)

            # Créer la compétence
            competence = Competence(
                duree=-1,  # -1 = passif permanent
                phase=phase,
                nom_effet=nom_comp.lower()
            )

            competences.append(competence)

        return competences

    def charger_tags(self, definition):
        """ Charge les tags depuis la définition JSON

        Args:
            definition: Dictionnaire contenant la définition de l'entité

        Returns:
            Liste de tags ou liste vide
        """
        tags = []

        if "tags" not in definition:
            return tags

        for tag_str in definition["tags"]:
            tag = Tag(tag_str)
            tags.append(tag)

        return tags

    def creer_creature(self, definition, pos, equipe):
        """Crée une instance de créature"""
        stats = definition["stats"]
        sprite_path = definition.get("sprite")
        carte_path = definition.get("carte")
        return Creature(
            nom=definition["nom"],
            pos=pos,
            equipe=equipe,
            pv=stats["pv"],
            cout=stats["cout"],
            combat=stats["combat"],
            demolition=stats["demolition"],
            degradation=stats["degradation"],
            portee=stats["portee"],
            control=stats["control"],
            mouv=stats["mouvement"],
            comp=self.charger_competences(definition),
            tags=self.charger_tags(definition),
            sprite_path=sprite_path,
            carte_path=carte_path
        )

    def creer_batiment(self, definition, pos, equipe):
        """Crée une instance de bâtiment"""
        stats = definition["stats"]
        sprite_path = definition.get("sprite")
        carte_path = definition.get("carte")

        return Batiment(
            nom=definition["nom"],
            pos=pos,
            equipe=equipe,
            pv=stats["pv"],
            cout=stats["cout"],
            combat=stats["combat"],
            demolition=stats["demolition"],
            degradation=stats["degradation"],
            portee=stats["portee"],
            control=stats["control"],
            comp=self.charger_competences(definition),
            tags=self.charger_tags(definition),
            sprite_path=sprite_path,
            carte_path=carte_path
        )

    def creer_case(self, definition, pos, equipe):
        """Crée une instance de case"""
        stats = definition["stats"]
        sprite_path = definition.get("sprite")
        carte_path = definition.get("carte")
        sprite_bg = definition.get("sprite_bg")
        sprite_fg = definition.get("sprite_fg")
        return Case(
            nom=definition["nom"],
            pos=pos,
            equipe=equipe,
            pv=stats["pv"],
            cout=stats["cout"],
            control_max=stats["control_max"],
            comp=self.charger_competences(definition),
            sprite_path=sprite_path,
            carte_path=carte_path,
            sprite_bg=sprite_bg,
            sprite_fg=sprite_fg,
            tags=self.charger_tags(definition)
        )

    def creer_sort(self, definition, pos, equipe):
        """Crée une instance de sort"""
        stats = definition["stats"]
        sprite_path = definition.get("sprite")
        carte_path = definition.get("carte")
        return Sort(
            nom=definition["nom"],
            pos=pos,
            equipe=equipe,
            cout=stats["cout"],
            comp=self.charger_competences(definition),
            sprite_path=sprite_path,
            carte_path=carte_path,
            tags=self.charger_tags(definition)
        )

""" Statut Chargeur """

import json
import os
from src.statut import StatutActif

class StatutChargeur:
    """Chargeur de statuts depuis des fichiers JSON."""

    def __init__(self, chemin_data="data/statuts", chemin_mods="mods"):
        self.chemin_data = chemin_data
        self.chemin_mods = chemin_mods
        self.statuts_chargees = {}
        self.mods_actifs = self.charger_mods_actifs()

    def charger_mods_actifs(self):
        """Retourne les dossiers de premier niveau présents dans le dossier des mods."""
        if not os.path.exists(self.chemin_mods):
            return []

        mods = []
        for entree in os.scandir(self.chemin_mods):
            if entree.is_dir():
                mods.append(entree.name)

        return mods

    def charger_tous_les_statuts(self):
        """Charge tous les statuts depuis data/ et mods/."""
        self.charger_depuis_dossier(self.chemin_data)

        for mod in self.mods_actifs:
            self.charger_depuis_dossier(os.path.join(self.chemin_mods, mod, "data", "statuts"))

    def charger_depuis_dossier(self, chemin):
        """Parcourt récursivement un dossier et charge tous les JSON de statut."""
        if not os.path.exists(chemin):
            return

        for root, _, files in os.walk(chemin):
            for fichier in files:
                if fichier.endswith(".json"):
                    chemin_complet = os.path.join(root, fichier)
                    self.charger_statut(chemin_complet)

    def charger_statut(self, fichier_json):
        """Charge un statut depuis un fichier JSON."""
        with open(fichier_json, "r", encoding="utf-8") as f:
            definition = json.load(f)

        definition_normalisee = StatutActif.normaliser_definition(definition, source=fichier_json)
        self.statuts_chargees[definition_normalisee["id"]] = definition_normalisee

    def creer_statut(self, id_statut):
        """Crée une instance de statut depuis son identifiant."""
        return StatutActif.depuis_id(id_statut)

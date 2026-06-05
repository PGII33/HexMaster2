""" Effet Chargeur """

import json
import os
from src.phase import PhaseTour

class EffetChargeur:
    """Chargeur d'effets composés depuis des fichiers JSON."""

    def __init__(self, chemin_data="data/effets", chemin_mods="mods"):
        self.chemin_data = chemin_data
        self.chemin_mods = chemin_mods
        self.effets_chargees = {}
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

    def charger_tous_les_effets(self):
        """Charge tous les effets depuis data/ et mods/."""
        self.charger_depuis_dossier(self.chemin_data)

        for mod in self.mods_actifs:
            self.charger_depuis_dossier(os.path.join(self.chemin_mods, mod, "data", "effets"))

    def charger_depuis_dossier(self, chemin):
        """Parcourt récursivement un dossier et charge tous les JSON d'effets."""
        if not os.path.exists(chemin):
            return

        for root, _, files in os.walk(chemin):
            for fichier in files:
                if fichier.endswith(".json"):
                    chemin_complet = os.path.join(root, fichier)
                    self.charger_effet(chemin_complet)

    def charger_effet(self, fichier_json):
        """Charge un effet composé depuis un fichier JSON."""
        with open(fichier_json, "r", encoding="utf-8") as f:
            definition = json.load(f)

        id_effet = definition.get("id")
        if not id_effet:
            raise ValueError(f"Effet invalide sans 'id': {fichier_json}")

        phase_str = definition.get("phase")
        if phase_str is None:
            raise ValueError(f"Effet '{id_effet}' invalide: champ 'phase' manquant")

        if not hasattr(PhaseTour, phase_str):
            raise ValueError(
                f"Effet '{id_effet}' invalide: phase inconnue '{phase_str}'"
            )

        definition["id"] = id_effet.lower()
        self.effets_chargees[definition["id"]] = definition

    def get_phase_effet(self, nom_effet):
        """Retourne la phase associée à un effet JSON, sinon None."""
        if nom_effet is None:
            return None

        definition = self.effets_chargees.get(nom_effet.lower())
        if definition is None:
            return None

        return getattr(PhaseTour, definition["phase"], None)
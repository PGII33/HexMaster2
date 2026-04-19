""" Fichier de lecture écriture des différentes valeurs utiles au son """

from __future__ import annotations
import json

class ParametresAudioStore:
    """ Classe de gestion de la sauvegarde et du chargement des paramètres audio"""
    def __init__(self, chemin_fichier:str):
        self._chemin_fichier = chemin_fichier
    
    def load(self) -> dict:
        """Charge les paramètres audio depuis le fichier, ou retourne un dictionnaire vide si le fichier n'existe pas ou est invalide."""
        try:
            with open(self._chemin_fichier, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise TypeError("Données de volume doivent être un dictionnaire.")
                return data
        except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
            print(f"Erreur chargement paramètres audio: {e}")
            print("Utilisation des valeurs par défaut.")
            return {}
    
    def save(self, data: dict) -> None:
        """Sauvegarde les paramètres audio dans le fichier."""
        try:
            with open(self._chemin_fichier, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Erreur sauvegarde paramètres audio: {e}")

    def load_into_manager(self, son_manager: SonManager) -> None:
        """Charge les paramètres audio depuis le fichier et les applique au SonManager."""
        data = self.load()
        son_manager.from_dict(data)
    
    def save_from_manager(self, son_manager: SonManager) -> None:
        """Récupère les paramètres audio du SonManager et les sauvegarde dans le fichier."""
        data = son_manager.to_dict()
        self.save(data)
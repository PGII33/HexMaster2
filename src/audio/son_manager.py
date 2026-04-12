"""Gestionnaire audio du jeu."""

from __future__ import annotations
from pathlib import Path
import pygame


class SonManager:
    """Gestionnaire simple pour les effets sonores et la musique."""

    def __init__(self, assets_dir: str | Path | None = None):
        self._assets_dir = Path(assets_dir) if assets_dir is not None else Path(__file__).resolve().parents[2] / "assets"
        self._sons: dict[str, pygame.mixer.Sound] = {}
        self._volume_global: float = 1.0
        self._volume_sfx: float = 1.0
        self._volume_musique: float = 1.0
        self._mixer_initialise = False

    def initialiser(self) -> None:
        """Initialise pygame.mixer si nécessaire."""
        if self._mixer_initialise:
            return

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self._mixer_initialise = True

    def chemin(self, *parties: str) -> Path:
        """Construit un chemin absolu vers un fichier de ressources."""
        return self._assets_dir.joinpath(*parties)

    def charger_son(self, nom: str, chemin: str | Path) -> pygame.mixer.Sound | None:
        """Charge un effet sonore et le met en cache."""
        self.initialiser()

        chemin_son = Path(chemin)
        if not chemin_son.is_absolute():
            chemin_son = self._assets_dir / chemin_son

        if not chemin_son.exists():
            print(f"Son introuvable: {chemin_son}")
            return None

        try:
            son = pygame.mixer.Sound(str(chemin_son))
        except pygame.error as erreur:
            print(f"Erreur chargement son {chemin_son}: {erreur}")
            return None

        son.set_volume(self._volume_global * self._volume_sfx)
        self._sons[nom] = son
        return son

    def get_son(self, nom: str) -> pygame.mixer.Sound | None:
        """Retourne un son déjà chargé."""
        return self._sons.get(nom)

    def jouer_son(self, nom: str) -> None:
        """Joue un effet sonore déjà chargé."""
        son = self._sons.get(nom)
        if son is None:
            print(f"Son non chargé: {nom}")
            return

        son.set_volume(self._volume_global * self._volume_sfx)
        son.play()

    def charger_musique(self, chemin: str | Path) -> Path | None:
        """ Charge une musique (ne mets pas en cache)"""
        self.initialiser()

        chemin_musique = Path(chemin)
        if not chemin_musique.is_absolute():
            chemin_musique = self._assets_dir / chemin_musique

        if not chemin_musique.exists():
            print(f"Musique introuvable: {chemin_musique}")
            return None

        return chemin_musique

    def jouer_musique(self, chemin: str | Path, boucle: int = -1, volume: float | None = None) -> None:
        """Charge et lance une musique de fond."""
        chemin_musique = self.charger_musique(chemin)
        if chemin_musique is None:
            return

        try:
            pygame.mixer.music.load(str(chemin_musique))
            pygame.mixer.music.set_volume(self._volume_global * self._volume_musique if volume is None else volume)
            pygame.mixer.music.play(boucle)
        except pygame.error as erreur:
            print(f"Erreur lecture musique {chemin_musique}: {erreur}")

    def arreter_musique(self) -> None:
        """Stoppe la musique de fond."""
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def pause_musique(self) -> None:
        """Met la musique en pause."""
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()

    def reprendre_musique(self) -> None:
        """Reprend la musique après une pause."""
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()

    def definir_volume_global(self, volume: float) -> None:
        """Définit le volume global sur une valeur entre 0 et 1."""
        self._volume_global = max(0.0, min(1.0, volume))
        self._appliquer_volumes()

    def definir_volume_sfx(self, volume: float) -> None:
        """Définit le volume des effets sonores."""
        self._volume_sfx = max(0.0, min(1.0, volume))
        self._appliquer_volumes()

    def definir_volume_musique(self, volume: float) -> None:
        """Définit le volume de la musique."""
        self._volume_musique = max(0.0, min(1.0, volume))
        self._appliquer_volumes()

    def couper_son(self) -> None:
        """Coupe tous les sons et la musique."""
        if pygame.mixer.get_init():
            pygame.mixer.stop()
            pygame.mixer.music.stop()

    def _appliquer_volumes(self) -> None:
        """Applique les volumes aux ressources déjà chargées."""
        volume_sfx = self._volume_global * self._volume_sfx
        for son in self._sons.values():
            son.set_volume(volume_sfx)

        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self._volume_global * self._volume_musique)

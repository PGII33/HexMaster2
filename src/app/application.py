""" Classe principale de l'application"""
import pygame
from pathlib import Path
from .ecrans.base_ecran import BaseEcran
from .ecrans.ecran_accueil import EcranAccueil
from .ecrans.ecran_parametres import EcranParametres
from .ecrans.ecran_credits import EcranCredits
from .ecrans.ecran_jeu import EcranJeu
from src.audio.son_manager import SonManager

from src.demo import creer_demo
from src.playground import creer_playground


class Application:
    """ Classe principale de l'application"""
    def __init__(self, ecran_initial:str):
        self._assets_dir = Path(__file__).resolve().parents[2] / "assets"
        self.FPS = 60
        self._ecrans: dict[str, BaseEcran] = {}
        pygame.init()
        self._width = 1280
        self._height = 720
        pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("HexMaster 2")
        pygame.display.set_icon(pygame.image.load(self._assets_dir / "autre" / "icon.png"))

        self._son_manager = SonManager(self._assets_dir)
        self._son_manager.initialiser()
        self._son_manager.charger_son("ui_click", Path("son") / "sfx" / "ui" / "click.mp3")
        self._playlist_musiques = [
            Path("son") / "musiques" / "acalmie.mp3",
            Path("son") / "musiques" / "serenite.mp3",
            Path("son") / "musiques" / "fantaisie.mp3",
        ]
        self._index_musique = 0
        self._event_fin_musique = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self._event_fin_musique)
        
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._running: bool = True

        self.creer_ecran("accueil", EcranAccueil(self._width, self._height, self._son_manager))
        self.creer_ecran("parametres", EcranParametres(self._width, self._height, self._son_manager))
        self.creer_ecran("demo", EcranJeu(self._width, self._height, creer_demo(), self._son_manager))
        self.creer_ecran("playground", EcranJeu(self._width, self._height, creer_playground(), self._son_manager))
        self.creer_ecran("credits", EcranCredits(self._width, self._height, self._son_manager))
        if ecran_initial not in self._ecrans:
            raise ValueError(f"Ecran initial '{ecran_initial}' non trouvé parmi les écrans disponibles")
        self._ecran_actuel: BaseEcran = self._ecrans[ecran_initial] 
        self._jouer_musique_suivante()

    def creer_ecran(self, nom:str, ecran:BaseEcran):
        """ Ajouter un écran au dictionnaire des écrans disponibles"""
        self._ecrans[nom] = ecran
    
    def changer_ecran(self, nom:str):
        """ Changer l'écran actuel"""
        if nom in self._ecrans:
            self._ecran_actuel = self._ecrans[nom]
        else:
            raise ValueError(f"Ecran '{nom}' non trouvé dans les écrans disponibles")

    def _jouer_musique_suivante(self) -> None:
        """Joue la prochaine musique de la playlist globale."""
        if not self._playlist_musiques:
            return

        chemin_musique = self._playlist_musiques[self._index_musique]
        self._son_manager.jouer_musique(chemin_musique, boucle=0)
        self._index_musique = (self._index_musique + 1) % len(self._playlist_musiques)
        
    def get_ecran_actuel(self) -> BaseEcran:
        """ Retourner l'écran actuel"""
        return self._ecran_actuel
    
    def lancer(self):
        """ Lancer la boucle principale de l'application"""
        while self._running:
            dt = self._clock.tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == self._event_fin_musique:
                    self._jouer_musique_suivante()
            self._ecran_actuel.handle_events(events)
            self._ecran_actuel.update(dt)
            self._ecran_actuel.afficher(pygame.display.get_surface())

            prochain_ecran: str|None = self._ecran_actuel.transition()
            if prochain_ecran:
                if prochain_ecran == "quit":
                    self._running = False
                else:
                    self.changer_ecran(prochain_ecran)
            pygame.display.flip()
        pygame.quit()
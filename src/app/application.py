""" Classe principale de l'application"""
import pygame
from .ecrans.base_ecran import BaseEcran
from .ecrans.ecran_accueil import EcranAccueil
from .ecrans.ecran_parametres import EcranParametres

class Application:
    """ Classe principale de l'application"""
    def __init__(self, ecran_initial:str):
        self.FPS = 60
        self._ecrans: dict[str, BaseEcran] = {}
        pygame.init()
        self._width = 1280
        self._height = 720
        pygame.display.set_mode((self._width, self._height))
        
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._running: bool = True

        self.creer_ecran("accueil", EcranAccueil(self._width, self._height))
        self.creer_ecran("parametres", EcranParametres(self._width, self._height))
        if ecran_initial not in self._ecrans:
            raise ValueError(f"Ecran initial '{ecran_initial}' non trouvé parmi les écrans disponibles")
        self._ecran_actuel: BaseEcran = self._ecrans[ecran_initial] 

    def creer_ecran(self, nom:str, ecran:BaseEcran):
        """ Ajouter un écran au dictionnaire des écrans disponibles"""
        self._ecrans[nom] = ecran
    
    def changer_ecran(self, nom:str):
        """ Changer l'écran actuel"""
        if nom in self._ecrans:
            self._ecran_actuel = self._ecrans[nom]
        else:
            raise ValueError(f"Ecran '{nom}' non trouvé dans les écrans disponibles")
        
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
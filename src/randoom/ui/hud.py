from __future__ import annotations
from typing import TYPE_CHECKING
from ..config import SCREEN_HEIGHT, SCREEN_WIDTH
from .minimapa import Minimapa
import pygame

if TYPE_CHECKING:
    from ..scenes import Mapa
    from ..entities import Jogador
    from ..entities import Sprite

class Hud:
    """
        Classe responsável por gerenciar a hud do jogador.
    """
    
    def __init__(self, surface: pygame.Surface, escala: int, mapa: Mapa, sprites: list[Sprite]):
        self.tela = surface
        self.mapa = mapa
        self.ESCALA = escala
        self.exibir_minimapa = True
        self.minimapa = Minimapa(mapa, escala, sprites)

    def desenharMinimapa(self, player: Jogador) -> None:
        self.minimapa.renderizar(self.tela, player)
        
    def indicarDano(self) -> None:
        indicador = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        indicador.set_alpha(100)
        indicador.fill("red")
        
        self.tela.blit(indicador, (0,0))
from __future__ import annotations
from typing import TYPE_CHECKING
from .minimapa import Minimapa
import pygame

if TYPE_CHECKING:
    from ..scenes import Mapa
    from ..entities import Jogador

class Hud:
    def __init__(self, surface: pygame.Surface, escala: int, mapa: Mapa):
        self.tela = surface
        self.mapa = mapa
        self.ESCALA = escala
        self.exibir_minimapa = True
        self.minimapa = Minimapa(mapa, escala)

    def desenharMinimapa(self, player: Jogador) -> None:
        self.minimapa.renderizar(self.tela, player)
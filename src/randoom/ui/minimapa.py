from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..scenes import Mapa
    from ..entities import Jogador

class Minimapa:
    def __init__(self, mapa: Mapa, escala: int) -> None:
        self.mapa = mapa
        self.ESCALA = escala

    def renderizar(self, tela: pygame.Surface, player: Jogador) -> None:
        for my, linha in enumerate(self.mapa.DESENHO):
            for mx, c in enumerate(linha):
                if c == "#":
                    bloco = (mx * self.ESCALA, my * self.ESCALA, self.ESCALA, self.ESCALA)
                    pygame.draw.rect(tela, "gray40", bloco)
                        
        pygame.draw.circle(tela, "white", (player.x * self.ESCALA, player.y * self.ESCALA), 5)
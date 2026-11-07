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
        superficie = pygame.Surface(tela.size, pygame.SRCALPHA)
        for my, linha in enumerate(self.mapa.DESENHO):
            for mx, c in enumerate(linha):
                bloco = (mx * self.ESCALA, my * self.ESCALA, self.ESCALA, self.ESCALA)
                if c == "#":
                    pygame.draw.rect(superficie, (120, 120, 120, 128), bloco)
                else:
                    pygame.draw.rect(superficie, (0, 0, 0, 128), bloco)
        
        tela.blit(superficie, (0, 0))
        pygame.draw.circle(tela, "white", (player.x * self.ESCALA, player.y * self.ESCALA), 5)
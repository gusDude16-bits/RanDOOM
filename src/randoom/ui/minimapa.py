from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from ..entities import Inimigo

if TYPE_CHECKING:
    from ..scenes import Mapa
    from ..entities import Jogador

class Minimapa:
    """
        Classe responsável por gerenciar o minimapa da Hud.
    """
    
    def __init__(self, mapa: Mapa, escala: int, entidades: list) -> None:
        self.mapa = mapa
        self.ESCALA = escala
        self.entidades = entidades

    def renderizar(self, tela: pygame.Surface, player: Jogador) -> None:
        superficie = pygame.Surface((tela.get_width(), tela.get_height()), pygame.SRCALPHA)
        for my, linha in enumerate(self.mapa.DESENHO):
            for mx, c in enumerate(linha):
                bloco = (mx * self.ESCALA, my * self.ESCALA, self.ESCALA, self.ESCALA)
                if c == "#":
                    pygame.draw.rect(superficie, (120, 120, 120, 128), bloco)
                else:
                    pygame.draw.rect(superficie, (0, 0, 0, 128), bloco)
        
        tela.blit(superficie, (0, 0))
        pygame.draw.circle(tela, "white", (player.x * self.ESCALA, player.y * self.ESCALA), 5)
        
        for entidade in self.entidades:
            if isinstance(entidade, Inimigo):
                pygame.draw.circle(tela, "red", (entidade.x * self.ESCALA, entidade.y * self.ESCALA), 5)
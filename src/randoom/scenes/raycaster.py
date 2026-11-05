from __future__ import annotations
import pygame
import math
from typing import TYPE_CHECKING
from ..config import SCREEN_HEIGHT, SCREEN_WIDTH

if TYPE_CHECKING:
    from ..entities import Jogador
    from .mapa import Mapa

class Raycaster:
    def __init__(self, surface: pygame.Surface, colunas: int) -> None:
        self.tela = surface
        self.colunas = colunas
        self.largura_tela = SCREEN_WIDTH
        self.altura_tela = SCREEN_HEIGHT
        self.largura_coluna = self.largura_tela // self.colunas

    def raycasting(self, player: Jogador, mapa: Mapa, escala: int) -> None:
        for i in range(self.colunas):
            angulo_raio = player.angulo - player.FOV / 2 + player.FOV * i / self.colunas
            distancia_real, lado = mapa.raio(angulo_raio, player.x, player.y)

            # Ponto (x,y) onde o raio bateu:
            px = player.x + distancia_real * math.cos(angulo_raio)
            py = player.y + distancia_real * math.sin(angulo_raio)

            # Correção do efeito "olho de peixe":
            distancia_raio = distancia_real * math.cos(angulo_raio - player.angulo)

            luz = max(30, 230 - distancia_raio * 22)

            if lado == 0:
                luz *= 0.7

            altura = min(self.altura_tela, self.altura_tela / distancia_raio)
            y_top = (self.altura_tela / 2 - altura / 2) + player.offset_caminhada
            y_base = (self.altura_tela / 2 + altura / 2) + player.offset_caminhada

            cor = (luz, luz * 0.9, luz * 0.75)
            faixa = (
                i * self.largura_coluna,
                min(y_top, y_base),
                self.largura_coluna,
                altura
            )

            pygame.draw.rect(self.tela, cor, faixa)
            pygame.draw.line(
                self.tela,
                "yellow",
                (player.x * escala, player.y * escala),
                (px * escala, py * escala)
            )
from __future__ import annotations
import pygame
import math
from typing import TYPE_CHECKING
from ..config import SCREEN_HEIGHT, SCREEN_WIDTH


if TYPE_CHECKING:
    from ..entities import Jogador
    from .mapa import Mapa
    from ..entities import Sprite

class Raycaster:
    def __init__(self, surface: pygame.Surface, colunas: int) -> None:
        self.tela = surface
        self.colunas = colunas                                                      # Colunas
        self.largura_tela = SCREEN_WIDTH
        self.altura_tela = SCREEN_HEIGHT
        self.largura_coluna = self.largura_tela // self.colunas                     # Pixels
        self.zBuffer = [0] * self.colunas

    def raycasting(self, player: Jogador, mapa: Mapa, escala: int, debug_ativado: bool) -> None:
        for i in range(self.colunas):
            angulo_raio = player.angulo - player.FOV / 2 + player.FOV * i / self.colunas
            distancia_real, lado = mapa.raio(angulo_raio, player.x, player.y)

            # Correção do efeito "olho de peixe":
            distancia_raio = distancia_real * math.cos(angulo_raio - player.angulo)
            self.zBuffer[i] = distancia_raio 
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
            
            # Ponto (x,y) onde o raio bateu:
            if debug_ativado is True:
                px = player.x + distancia_real * math.cos(angulo_raio)
                py = player.y + distancia_real * math.sin(angulo_raio)
                
                if pygame.key.get_pressed()[pygame.K_TAB] == 1:
                    pygame.draw.line(
                        self.tela,
                        "yellow",
                        (player.x * escala, player.y * escala),
                        (px * escala, py * escala)
                    )

    def desenhar_sprite(self, sprite: Sprite, player: Jogador):
        angulo_relativo = sprite.anguloRelativo(player)
        
        if not(- math.pi / 2 < angulo_relativo < math.pi / 2):
            return  # Se não estiver no campo de visão, n faz nada
        
        distancia_real = math.sqrt(sprite.distancia(player))
        distancia_raio_sprite = abs(distancia_real * math.cos(angulo_relativo))

        # Dimensões do sprite
        altura_sprite = min(self.altura_tela, self.altura_tela / distancia_raio_sprite)
        proporcao = sprite.imagem.get_width() / sprite.imagem.get_height()
        largura_sprite = altura_sprite * proporcao

        coluna = (angulo_relativo + player.FOV / 2) * self.colunas / player.FOV

        centro_px = coluna * self.largura_coluna        # Pixels
        esquerda = centro_px - largura_sprite / 2       # Pixels
        direita = centro_px + largura_sprite / 2        # Pixels

        y_top = self.altura_tela / 2 - altura_sprite / 2 + player.offset_caminhada

        imagem = pygame.transform.scale(sprite.imagem, (int(largura_sprite), int(altura_sprite)))
        for i in range(int(max(esquerda / self.largura_coluna, 0)), int(min(direita / self.largura_coluna, self.colunas))):
            if self.zBuffer[i] > distancia_raio_sprite:
                posicao_na_tela = (
                    i * self.largura_coluna,
                    y_top,
                )

                faixa_da_imagem = (
                    i * self.largura_coluna - esquerda,     # Posição X na imagem
                    0,                                      # Posição Y na imagem
                    self.largura_coluna,
                    altura_sprite
                )

                self.tela.blit(imagem, posicao_na_tela, faixa_da_imagem)
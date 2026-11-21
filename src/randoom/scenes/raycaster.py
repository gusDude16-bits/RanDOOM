from __future__ import annotations
import pygame
import math
import random
from typing import TYPE_CHECKING
from ..config import SCREEN_HEIGHT, SCREEN_WIDTH

if TYPE_CHECKING:
    from ..entities import Jogador, Sprite
    from .mapa import Mapa
    from pathlib import Path

class Raycaster:
    def __init__(self, surface: pygame.Surface, colunas: int, caminhos_paredes: list[Path]) -> None:
        self.tela = surface
        self.colunas = colunas
        self.largura_tela = SCREEN_WIDTH
        self.altura_tela = SCREEN_HEIGHT
        self.largura_coluna = self.largura_tela // self.colunas
        self.zBuffer = [0] * self.colunas
        
        self.texturas_paredes: list[pygame.Surface] = []
        
        for path in caminhos_paredes:
            self.texturas_paredes.append(pygame.image.load(path).convert())
            
        self.tex_largura = self.texturas_paredes[0].get_width()
        self.tex_altura = self.texturas_paredes[0].get_height()
        
        self.textura_da_celula: dict[tuple[int, int], int] = {}

    def raycasting(self, player: Jogador, mapa: Mapa, escala: int, debug_ativado: bool) -> None:
        for i in range(self.colunas):
            angulo_raio = player.angulo - player.FOV / 2 + player.FOV * i / self.colunas
            distancia_real, lado, celula = mapa.raio(angulo_raio, player.x, player.y)

            # Correção do efeito "olho de peixe":
            distancia_raio = distancia_real * math.cos(angulo_raio - player.angulo)
            self.zBuffer[i] = distancia_raio 
            
            luz = max(30, 230 - distancia_raio * 22)
            
            # Ponto onde o raio bateu
            px = player.x + distancia_real * math.cos(angulo_raio)
            py = player.y + distancia_real * math.sin(angulo_raio)

            if lado == 0:
                luz *= 0.7
                pos_na_parede = py - math.floor(py)
            else:
                pos_na_parede = px - math.floor(px)
            
            # Escolho uma textura de parede aleatória para a célula do mapa
            if celula not in self.textura_da_celula:
                self.textura_da_celula[celula] = random.choices(
                    range(len(self.texturas_paredes)),
                    weights=(1, 2)
                )[0]

                
            textura = self.texturas_paredes[self.textura_da_celula[celula]]

            # Calcula a posição x da textura na coluna atual
            tex_x = int(pos_na_parede * self.tex_largura)

            altura = min(int(self.altura_tela / distancia_raio), self.altura_tela * 4)
            y_top = (self.altura_tela / 2 - altura / 2) + player.offset_caminhada
            
            fatia = textura.subsurface((tex_x, 0, 1, self.tex_altura))
            fatia = pygame.transform.scale(fatia, (self.largura_coluna, altura))
            fatia.fill((luz, luz, luz), special_flags=pygame.BLEND_MULT)
            
            self.tela.blit(fatia, (i * self.largura_coluna, y_top))
            
            # Ponto (x,y) onde o raio bateu:
            if debug_ativado is True:
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

        centro_px = coluna * self.largura_coluna
        esquerda = centro_px - largura_sprite / 2
        direita = centro_px + largura_sprite / 2

        y_top = self.altura_tela / 2 - altura_sprite / 2 + player.offset_caminhada

        imagem = pygame.transform.scale(sprite.imagem, (int(largura_sprite), int(altura_sprite)))
        for i in range(int(max(esquerda / self.largura_coluna, 0)), int(min(direita / self.largura_coluna, self.colunas))):
            if self.zBuffer[i] > distancia_raio_sprite:
                posicao_na_tela = (
                    i * self.largura_coluna,
                    y_top,
                )

                faixa_do_sprite = (
                    i * self.largura_coluna - esquerda,     # Posição X na imagem do sprite
                    0,                                      # Posição Y na imagem do sprite
                    self.largura_coluna,
                    altura_sprite
                )

                self.tela.blit(imagem, posicao_na_tela, faixa_do_sprite)
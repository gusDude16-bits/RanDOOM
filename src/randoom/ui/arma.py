from __future__ import annotations
from typing import TYPE_CHECKING
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, LARGURA_ARMA, ALTURA_ARMA
from pathlib import Path
import pygame
import math

if TYPE_CHECKING:
    from ..entities import Jogador

class Arma:
    def __init__(self, dano: int, velocidade: float, caminhos: list[Path]) -> None:
        temp = [pygame.image.load(path).convert_alpha() for path in caminhos]
        maior_altura = max(img.get_height() for img in temp)

        self.imagens = [pygame.transform.scale_by(img, (ALTURA_ARMA / maior_altura)) for img in temp]
        
        self.dano = dano
        self.vel = 1000 / velocidade # ms
        self.ultimo_tiro = - self.vel

        self.atirando = False

        self.IDLE = 0
        self.SEQUENCIA = [(1, 60), (2, 80), (3, 60), (4, 80), (5, 60)]

    def animacao_tiro(self, tela: pygame.Surface, tempo_atual: int, player: Jogador) -> None:
        decorrido = tempo_atual - self.ultimo_tiro
        frame = self.imagens[self.IDLE]

        acumulado = 0
        for indice, duracao in self.SEQUENCIA:
            acumulado += duracao
            if decorrido < acumulado:
                frame = self.imagens[indice]
                break

        # Movimentação enquanto o jogador anda
        intensidade_movimento = player.amplitude_balanco / 6

        dx = math.sin(player.fase_movimento / 2) * intensidade_movimento * 15 # px 
        dy = abs(math.sin(player.fase_movimento / 2)) * intensidade_movimento * 20 # px

        rect = frame.get_rect()
        rect.midbottom = (SCREEN_WIDTH // 2 - LARGURA_ARMA // 8 + dx, SCREEN_HEIGHT + dy)

        tela.blit(frame, rect)
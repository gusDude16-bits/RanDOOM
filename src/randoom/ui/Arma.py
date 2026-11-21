from pathlib import Path
import pygame
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, LARGURA_ARMA, ALTURA_ARMA

class Arma:
    def __init__(self, caminho_arma: Path):
        imagem = pygame.image.load(caminho_arma).convert_alpha()
        self.imagem = pygame.transform.scale(imagem, (LARGURA_ARMA, ALTURA_ARMA))
        self.rect = self.imagem.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.blit(self.imagem, self.rect)
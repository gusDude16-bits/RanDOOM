from ..config import CAMINHO_ARMA, SCREEN_WIDTH, SCREEN_HEIGHT, LARGURA_ARMA, ALTURA_ARMA
import pygame

class Arma:
    def __init__(self, dano: int, velocidade: float) -> None:
        self.imagem = pygame.image.load(CAMINHO_ARMA).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (LARGURA_ARMA, ALTURA_ARMA))
        
        self.rect = self.imagem.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)

        self.dano = dano
        self.vel = 1000 / velocidade # ms

        self.duracao_tiro = 600 # ms
        self.ultimo_tiro = - self.vel

        self.atirando = False
import pygame
import sys
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from .entities import Jogador
from .scenes import Mapa, Raycaster
from .ui import Hud

class Jogo:
    def __init__(self) -> None:
        pygame.init()
        
        pygame.display.set_caption(TITLE)
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.relogio = pygame.time.Clock()
        self.rodando: bool = True

        self.ESCALA = SCREEN_WIDTH // 75
        self.COLUNAS = SCREEN_WIDTH // 5
        self.LARGURA = SCREEN_WIDTH // self.COLUNAS

        self.player = Jogador(1.5, 6.5, 0.0)
        self.mapa = Mapa(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.raycaster = Raycaster(self.tela, self.COLUNAS)
        self.hud = Hud(self.tela, self.ESCALA, self.mapa)
    
    def checar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
    
    def atualizar(self) -> None:
        teclas = pygame.key.get_pressed()
                    
        giro = teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]
        frente = teclas[pygame.K_UP] - teclas[pygame.K_DOWN]
        correndo = teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]

        self.player.movimentar(self.mapa, frente, giro, correndo)
    
    def renderizar(self):
        self.tela.fill("gray10") # Teto
        pygame.draw.rect(self.tela, "sienna4", (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)) # Chão
        self.raycaster.raycasting(self.player, self.mapa, self.ESCALA)
        self.hud.desenharMinimapa(self.player)
        pygame.display.flip()
    
    def executar(self) -> None:                    
        while self.rodando:
            self.checar_eventos()
            self.atualizar()
            self.renderizar()
            self.relogio.tick(FPS)
        pygame.quit()
    
def main() -> None:
    RanDOOM = Jogo()
    RanDOOM.executar()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa Encerrado.")
import pygame
import math
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from .entities import Jogador, Sprite
from .scenes import Mapa, Raycaster
from .ui import Hud

class Jogo:
    def __init__(self) -> None:
        pygame.init()
        
        pygame.display.set_caption(TITLE)
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.relogio = pygame.time.Clock()
        self.rodando: bool = True
        self.debug_ativado: bool = False

        self.ESCALA = SCREEN_WIDTH // 75
        self.COLUNAS = SCREEN_WIDTH // 5
        self.LARGURA = SCREEN_WIDTH // self.COLUNAS

        self.player = Jogador(2.5, 6.5, 0.0)
        self.mapa = Mapa(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.raycaster = Raycaster(self.tela, self.COLUNAS)
        self.sprites = list()
        self.sprites.append(Sprite(4, 8, 0.0))
        self.hud = Hud(self.tela, self.ESCALA, self.mapa, self.sprites)
    
    def checar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                if evento.key == pygame.K_g:
                    if self.debug_ativado is False:
                        self.debug_ativado = True
                    else:
                        self.debug_ativado = False
    
    def atualizar(self) -> None:
        teclas = pygame.key.get_pressed()
        
        giro = teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]
        frente = teclas[pygame.K_UP] - teclas[pygame.K_DOWN]
        correndo = teclas[pygame.K_LCTRL] or teclas[pygame.K_RCTRL]

        self.player.movimentar(self.mapa, frente, giro, correndo)
    
    def renderizar(self):
        self.tela.fill("gray10") # Teto

        pygame.draw.rect(
            self.tela, 
            "sienna4", 
            (0, SCREEN_HEIGHT / 2 + self.player.offset_caminhada, SCREEN_WIDTH, SCREEN_HEIGHT)
        ) # Chão

        self.raycaster.raycasting(self.player, self.mapa, self.ESCALA, self.debug_ativado)
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.hud.desenharMinimapa(self.player)

        # angulo_relativo = self.sprites[0].anguloRelativo(self.player)
        # if (- self.player.FOV / 2) <= angulo_relativo < (self.player.FOV / 2):
        #     print(f"Coluna: {((angulo_relativo + self.player.FOV / 2) * self.COLUNAS / self.player.FOV)}")
        # else:
        #     print(f"Não aparece")
        
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
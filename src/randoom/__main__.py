import pygame
import sys
import math
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from .entities import Jogador
from .scenes import Mapa

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
            
    def raytracing(self):
        for i in range(self.COLUNAS):
            angulo_raio = self.player.angulo - self.player.FOV / 2 + self.player.FOV * i / self.COLUNAS
            distancia_real, lado = self.mapa.raio(angulo_raio, self.player.x, self.player.y)

            # Onde o raio bate:
            px = self.player.x + distancia_real * math.cos(angulo_raio)
            py = self.player.y + distancia_real * math.sin(angulo_raio)

            distancia_raio = distancia_real * math.cos(angulo_raio - self.player.angulo) # Corrige o efeito olho de peixe
            luz = max(30, 230 - distancia_raio * 22)

            if lado == 0:
                luz *= 0.7

            altura = min(SCREEN_HEIGHT, SCREEN_HEIGHT / distancia_raio)

            cor = (luz, luz * 0.9, luz * 0.75)
            faixa = (i * self.LARGURA, (SCREEN_HEIGHT - altura) / 2, self.LARGURA, altura)

            pygame.draw.rect(self.tela, cor, faixa) # Paredes
            pygame.draw.line(
                self.tela,
                "yellow",
                (self.player.x * self.ESCALA, self.player.y * self.ESCALA),
                (px * self.ESCALA, py * self.ESCALA)
            ) # Raios
    
    def renderizar(self):
        self.tela.fill("gray10") # Teto
        pygame.draw.rect(self.tela, "sienna4", (0, 200, 600, 200)) # Chão
        self.raytracing()

        for my, linha in enumerate(self.mapa.DESENHO):
            for mx, c in enumerate(linha):
                if c == "#":
                    bloco = (mx * self.ESCALA, my * self.ESCALA, self.ESCALA, self.ESCALA)
                    pygame.draw.rect(self.tela, "gray40", bloco)
                        
        pygame.draw.circle(self.tela, "white", (self.player.x * self.ESCALA, self.player.y * self.ESCALA), 5)
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
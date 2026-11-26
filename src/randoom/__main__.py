import pygame
import random
import math
from .config import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    FPS, 
    TITLE, 
    CAMINHO_PAREDE_LIMPA, 
    CAMINHO_PAREDE, 
    CAMINHO_CEU,
    CAMINHO_INIMIGO,
)
from .entities import Jogador, Sprite, Inimigo
from .scenes import Mapa, Raycaster
from .ui import Hud, Arma

class Jogo:
    """
        Classe responsável por controlar os principais aspectos do jogo 
        por meio da biblioteca pygame.
    """
    
    def __init__(self) -> None:
        pygame.init()
        
        pygame.display.set_caption(TITLE)
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.relogio = pygame.time.Clock()
        self.rodando: bool = True
        self.debug_ativado: bool = False

        # Cooldown de dano
        self.cooldown_dano = 800 # ms
        self.ultimo_dano = -self.cooldown_dano

        # Indicador de dano
        self.duracao_flash = 400 # ms
        self.ultimo_flash = -self.duracao_flash
        
        # Screen Shake
        self.duracao_shake = 300 # ms
        self.intensidade_shake = 8 # px

        self.ESCALA = SCREEN_WIDTH // 75
        self.COLUNAS = SCREEN_WIDTH // 5
        self.LARGURA = SCREEN_WIDTH // self.COLUNAS
        self.paredes = [CAMINHO_PAREDE, CAMINHO_PAREDE_LIMPA]

        self.player = Jogador(1.5, 6.5, 0.0, 100)
        self.mapa = Mapa()
        self.entidades = []
        self.raycaster = Raycaster(self.tela, self.COLUNAS, self.paredes)
        self.hud = Hud(self.tela, self.ESCALA, self.mapa, self.entidades)
        self.armas: list[Arma] = []
        
        self.entidades.append(Inimigo(6, 7, 0, 100, 50, CAMINHO_INIMIGO))
        self.armas.append(Arma(10, 5))
            
    def checar_eventos(self) -> None:
        """
            Verifica se o jogo deve ser encerrado com base nos eventos 
            que ocorrem dentro do loop.
        """
        
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
            
            # if self.player.isDead():
            #     self.rodando = False
    
    def atualizar(self) -> None:
        """
            Gerencia as interações jogador-jogo no loop principal.
        """

        tempo_atual = pygame.time.get_ticks()
        teclas = pygame.key.get_pressed()
        
        giro = teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]
        frente = teclas[pygame.K_UP] - teclas[pygame.K_DOWN]
        correndo = teclas[pygame.K_LCTRL] or teclas[pygame.K_RCTRL]

        if teclas[pygame.K_i]:
            temp = Inimigo(
                random.randint(1, 6),
                random.randint(1, 6),
                0.0, 
                100, 
                10, 
                CAMINHO_INIMIGO
            )
            self.entidades.append(temp)

        self.player.movimentar(self.mapa, frente, giro, correndo)

        arma = self.armas[0]
        arma.atirando = False

        if teclas[pygame.K_SPACE] and tempo_atual - arma.ultimo_tiro >= arma.vel:
            arma.atirando = True
            arma.ultimo_tiro = tempo_atual
        
        for entidade in self.entidades:
            if isinstance(entidade, Inimigo):
                entidade.movimentar(self.player, self.mapa)
        
                if entidade.contatoJogador(self.player) and tempo_atual - self.ultimo_dano >= self.cooldown_dano:
                    self.ultimo_dano = tempo_atual
                    self.player.hp -= entidade.dano
                    self.ultimo_flash = tempo_atual

        if self.armas[0].atirando:
            no_alcance = [e for e in self.entidades if isinstance(e, Inimigo) and e.acertou(self.player)]

            if no_alcance:
                alvo = min(no_alcance, key = lambda e: e.sprite.distancia(self.player))
                alvo.hp -= self.armas[0].dano
            
        self.entidades[:] = [e for e in self.entidades if isinstance(e, Inimigo) and not e.isDead()]
    
    def renderizar(self):
        """
            Renderiza o jogo com base no estado atual.
        """
        
        tempo_atual = pygame.time.get_ticks()
        self.tela.fill("#09005e") # Teto
        
        pygame.draw.rect(
            self.tela, 
            "#464646", 
            (0, SCREEN_HEIGHT / 2 + self.player.offset_caminhada, SCREEN_WIDTH, SCREEN_HEIGHT)
        ) # Chão

        self.raycaster.raycasting(self.player, self.mapa, self.ESCALA, self.debug_ativado)

        self.entidades.sort(key= lambda e: e.sprite.distancia(self.player), reverse=True)
        for entidade in self.entidades:
            if isinstance(entidade, Inimigo):
                if not entidade.isDead():
                    self.raycaster.desenhar_sprite(entidade.sprite, self.player)

        self.tela.blit(self.armas[0].imagem, self.armas[0].rect)

        tempo_decorrido = tempo_atual - self.ultimo_flash
        
        if tempo_decorrido < self.duracao_flash:
            self.hud.indicarDano()
        
        if tempo_decorrido < self.duracao_shake:
            forca = self.intensidade_shake * (1 - tempo_decorrido / self.duracao_shake)
            dx = random.randint(-int(forca), int(forca))
            dy = random.randint(-int(forca), int(forca))

            copia = self.tela.copy()
            self.tela.fill("#000000")
            self.tela.blit(copia, (dx, dy))

        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.hud.desenharMinimapa(self.player)

        pygame.display.flip()
    
    def executar(self) -> None:
        """
            Loop principal do jogo
        """
                           
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
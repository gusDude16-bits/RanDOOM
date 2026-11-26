import pygame
import random
from .config import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    FPS, 
    TITLE, 
    CAMINHO_PAREDE_LIMPA, 
    CAMINHO_PAREDE, 
    CAMINHO_CEU,
    CAMINHO_INIMIGO
)
from .entities import Jogador, Sprite, Inimigo
from .scenes import Mapa, Raycaster
from .ui import Hud

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
        self.mapa = Mapa(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.sprites: list[Sprite] = []
        self.entidades = []
        self.raycaster = Raycaster(self.tela, self.COLUNAS, self.paredes)
        self.hud = Hud(self.tela, self.ESCALA, self.mapa, self.sprites)
        
        self.entidades.append(Inimigo(6, 7, 0, 100, 10, CAMINHO_INIMIGO))
        self.sprites.append(self.entidades[0].sprite)
            
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

        self.player.movimentar(self.mapa, frente, giro, correndo)
        
        for entidade in self.entidades:
            if isinstance(entidade, Inimigo):
                entidade.movimentar(self.player, self.mapa)
                
                if entidade.contatoJogador(self.player) and tempo_atual - self.ultimo_dano >= self.cooldown_dano:
                    self.ultimo_dano = tempo_atual
                    self.player.hp -= entidade.dano
                    self.ultimo_flash = tempo_atual
    
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
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.hud.desenharMinimapa(self.player)
        
        for sprite in self.sprites:
            self.raycaster.desenhar_sprite(sprite, self.player)
        
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
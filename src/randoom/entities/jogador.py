from ..config import DEFAULT_FOV, DEFAULT_SPEED
from ..scenes import Mapa
from .entity import Entity
import math

class Jogador (Entity):
    """
        Classe jogador, responsável por guardar posição, campo de visão e
        controlar a movimentação e o hp restante do jogador.
    """

    def __init__(self, px: float, py: float, angulo: float, hp: int, FOV: float = DEFAULT_FOV) -> None:
        super().__init__(px, py, angulo)
        
        self.FOV = FOV
        self.velocidade = DEFAULT_SPEED
        self.hp = hp
        
        self.fase_movimento = 0.0   # Em que fase da função seno que descreve o balanço da visão do jogador está
        self.amplitude_balanco = 0.0
        self.velocidade_balanco = 0.4

    def isDead(self) -> bool:
        return self.hp <= 0

    def movimentar(self, mapa: Mapa, frente: int, giro: int, correndo: bool) -> None:
        passo = frente * (self.velocidade if not correndo else self.velocidade * 1.6)
        self.angulo += giro * 0.1

        dx = math.cos(self.angulo) * passo
        dy = math.sin(self.angulo) * passo

        if not mapa.parede(self.x + dx, self.y):
            self.x += dx
        if not mapa.parede(self.x, self.y + dy):
            self.y += dy

        # Velocidade e Amplitude alvo para a função de balanço de visão
        if frente != 0:
            velocidade_alvo = 0.6 if correndo else 0.4
            amplitude_alvo = 10 if correndo else 6

            self.fase_movimento += self.velocidade_balanco
        else:
            velocidade_alvo = 0.3
            amplitude_alvo = 0.0

        # Efeito de movimento
        self.amplitude_balanco += (amplitude_alvo - self.amplitude_balanco) * 0.15
        self.velocidade_balanco += (velocidade_alvo - self.velocidade_balanco) * 0.15
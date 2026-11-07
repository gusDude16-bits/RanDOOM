from ..config import DEFAULT_FOV, DEFAULT_SPEED
from ..scenes import Mapa
from .entity import Entity
import math

class Jogador (Entity):
    """
        Classe jogador, responsável por guardar posição, campo de visão e
        controlar a movimentação.
    """

    def __init__(self, px: float, py: float, angulo: float, FOV: float = DEFAULT_FOV) -> None:
        super().__init__(px, py, angulo)
        
        self.FOV = FOV
        self.velocidade = DEFAULT_SPEED
        self.tempo_caminhada = 0.0
        self.offset_caminhada = 0.0

    def movimentar(self, mapa: Mapa, frente: int, giro: int, correndo: bool) -> None:
        passo = frente * (self.velocidade if not correndo else self.velocidade * 1.6)
        self.angulo += giro * 0.05

        dx = math.cos(self.angulo) * passo
        dy = math.sin(self.angulo) * passo

        if not mapa.parede(self.x + dx, self.y):
            self.x += dx
        if not mapa.parede(self.x, self.y + dy):
            self.y += dy

        # Efeito de movimento:
        if frente != 0:
            freq = 0.3 if correndo else 0.2
            amp = 12 if correndo else 6

            self.tempo_caminhada += freq
            self.offset_caminhada = math.sin(self.tempo_caminhada) * amp
        else:
            self.tempo_caminhada = 0
            self.offset_caminhada *= 0.8
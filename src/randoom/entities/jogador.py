from ..config import DEFAULT_FOV, DEFAULT_SPEED
from ..scenes import Mapa
import math

class Jogador:
    """
        Classe jogador, responsável por guardar posição, campo de visão e
        controlar a movimentação.
    """

    def __init__(self, px: float, py: float, angulo: float, FOV: float = DEFAULT_FOV) -> None:
        self.x = px
        self.y = py
        self.FOV = FOV
        self.angulo = angulo
        self.velocidade = DEFAULT_SPEED

    def movimentar(self, mapa: Mapa, frente: int, giro: int, correndo: bool) -> None:
        passo = frente * (self.velocidade if not correndo else self.velocidade * 2)
        self.angulo += giro * 0.05

        dx = math.cos(self.angulo) * passo
        dy = math.sin(self.angulo) * passo

        if not mapa.parede(self.x + dx, self.y):
            self.x += dx
        if not mapa.parede(self.x, self.y + dy):
            self.y += dy
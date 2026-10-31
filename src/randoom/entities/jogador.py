from ..config import DEFAULT_FOV
import math

class Jogador:
    """
        Classe jogador, responsável por guardar posição, campo de visão e
        controlar a movimentação.
    """

    def __init__(self, px: float, py: float, angulo: float, FOV: float) -> None:
        self.x = px
        self.y = py
        self.FOV = FOV
        self.angulo = angulo

    def novaPosicao(self, passo: int) -> tuple[float, float]:
        dx = math.cos(self.angulo) * passo
        dy = math.sin(self.angulo) * passo
        return dx, dy

    def girar(self, giro: float) -> None:
        self.angulo += giro
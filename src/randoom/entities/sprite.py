from __future__ import annotations
from typing import TYPE_CHECKING
from .entity import Entity
import math

if TYPE_CHECKING:
    from .jogador import Jogador

class Sprite (Entity):
    def __init__(self, x: float, y: float, angulo: float) -> None:
        super().__init__(x, y, angulo)

    def distancia(self, player: Jogador) -> float:
        return (self.x - player.x) * (self.x - player.x) + (self.y - player.y) * (self.y - player.y)

    def anguloRelativo(self, player: Jogador) -> float:
        dx = self.x - player.x
        dy = self.y - player.y
        return math.remainder((math.atan2(dy, dx) - player.angulo), math.pi * 2)
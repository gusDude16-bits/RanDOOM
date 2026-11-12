from __future__ import annotations
from typing import TYPE_CHECKING
from .entity import Entity
from .sprite import Sprite
from ..config import DEFAULT_SPEED
from pathlib import Path
import math

if TYPE_CHECKING:
    from jogador import Jogador
    from ..scenes import Mapa

class Inimigo (Entity):
    def __init__(self, x: float, y: float, angulo: float, hp: float, imagem: str, velocidade: float = DEFAULT_SPEED / 2) -> None:
        super().__init__(x, y, angulo)
        self.hp = hp
        self.velocidade = velocidade
        self.sprite = Sprite(x, y, angulo, imagem)

    def isDead(self) -> bool:
        return self.hp <= 0

    def movimentar(self, player: Jogador, mapa: Mapa):
        if self.sprite.distancia(player) <= 1:
            return

        angulo_ate_player = math.atan2(self.y - player.y, self.x - player.x)
        
        dx = math.cos(angulo_ate_player) * self.velocidade
        dy = math.sin(angulo_ate_player) * self.velocidade

        if not mapa.parede(self.x - dx, self.y):
            self.x -= dx
            self.sprite.x -= dx
        if not mapa.parede(self.x, self.y - dy):
            self.y -= dy
            self.sprite.y -= dy
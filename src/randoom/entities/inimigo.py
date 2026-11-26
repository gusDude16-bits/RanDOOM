from __future__ import annotations
from typing import TYPE_CHECKING
from .entity import Entity
from .sprite import Sprite
from ..config import DEFAULT_SPEED
import math

if TYPE_CHECKING:
    from jogador import Jogador
    from ..scenes import Mapa

class Inimigo (Entity):
    """
        Inimigo do jogo, capaz de se movimentar em direção 
        ao jogador e dar dano ao mesmo.
    """
    
    def __init__(self, x: float, y: float, angulo: float, hp: int, dano: int, imagem: str, velocidade: float = DEFAULT_SPEED / 2) -> None:
        super().__init__(x, y, angulo)
        self.hp = hp
        self.dano = dano
        self.velocidade = velocidade
        self.sprite = Sprite(x, y, angulo, imagem)

    def isDead(self) -> bool:
        return self.hp <= 0

    def contatoJogador(self, player: Jogador) -> bool:
        return self.sprite.distancia(player) <= 1

    def acertou(self, player: Jogador) -> bool:
        distancia = math.sqrt(self.sprite.distancia(player))
        limite = math.atan2(0.3, distancia)
        return abs(self.sprite.anguloRelativo(player)) <= limite

    def movimentar(self, player: Jogador, mapa: Mapa):
        if self.contatoJogador(player):
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
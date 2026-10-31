import random
import math

class Mapa:
    def __init__(self, dimensao_x: int, dimensao_y: int):
        self.DESENHO = [
            "###############",
            "#...##...###..#",
            "#.........#...#",
            "#....###.....##",
            "###.......##..#",
            "#.........##..#",
            "#...##........#",
            "##......####..#",
            "#.......##....#",
            "###############",
        ]
        
    def parede(self, px: int, py: int) -> bool:
        return self.DESENHO[int(py)][int(px)] == "#"

    def raio(self, angulo: float, x_i: float, y_i: float) -> tuple[float, int]:
        cos, sen = math.cos(angulo), math.sin(angulo)
        distancia = 0

        while not self.parede(x_i + cos * distancia, y_i + sen * distancia):
            distancia += 0.02

        # Verifica se tá do lado de uma parede: 
        x_antes = int(x_i + cos * (distancia - 0.02))
        x_bateu = int(x_i + cos * distancia)
        
        lado = 0 if x_antes != x_bateu else 1

        return distancia, lado
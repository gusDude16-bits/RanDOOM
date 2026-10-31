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

    def raio(self, angulo: float, x_i: float, y_i: float) -> float:
        cos, sen = math.cos(angulo), math.sin(angulo)
        distancia = 0

        while not self.parede(x_i + cos * distancia, y_i + sen * distancia):
            distancia += 0.02

        return distancia
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

    def raio(self, angulo: float, x_j: float, y_j: float) -> tuple[float, int]:
        cos, sen = math.cos(angulo), math.sin(angulo)

        passo_x = abs(1 / cos) if cos != 0 else math.inf
        passo_y = abs(1 / sen) if sen != 0 else math.inf

        map_x = math.floor(x_j)
        map_y = math.floor(y_j)

        inicial_x = map_x + 1 - x_j if cos > 0 else x_j - map_x
        inicial_y = map_y + 1 - y_j if sen > 0 else y_j - map_y

        dist_x = inicial_x * passo_x
        dist_y = inicial_y * passo_y

        while True:
            if dist_x < dist_y:
                dist_total = dist_x
                dist_x += passo_x
                map_x = map_x + 1 if cos > 0 else map_x - 1
                lado = 0
            else:
                dist_total = dist_y
                dist_y += passo_y
                map_y = map_y + 1 if sen > 0 else map_y - 1
                lado = 1

            if self.parede(map_x, map_y):
                return dist_total, lado
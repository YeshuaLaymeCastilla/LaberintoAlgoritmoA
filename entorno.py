import random

class EntornoDQN:
    def __init__(self, laberinto, inicio, meta):
        self.laberinto = laberinto
        self.inicio = inicio
        self.meta = meta
        self.estado = inicio

    def reset(self):
        self.estado = self.inicio
        return self.estado

    def mover(self, accion):
        fila, col = self.estado
        nuevo_estado = self.estado

        if accion == "arriba":
            nuevo_estado = (fila - 1, col)
        elif accion == "abajo":
            nuevo_estado = (fila + 1, col)
        elif accion == "izquierda":
            nuevo_estado = (fila, col - 1)
        elif accion == "derecha":
            nuevo_estado = (fila, col + 1)

        if not (0 <= nuevo_estado[0] < len(self.laberinto)) or not (0 <= nuevo_estado[1] < len(self.laberinto[0])):
            return self.estado, -5, False  # golpe fuera del mapa

        if self.laberinto[nuevo_estado[0]][nuevo_estado[1]] == 1:
            return self.estado, -5, False  # golpe contra obstáculo

        self.estado = nuevo_estado

        if self.estado == self.meta:
            return self.estado, 100, True  # llegó a la meta

        return self.estado, -1, False  # paso normal

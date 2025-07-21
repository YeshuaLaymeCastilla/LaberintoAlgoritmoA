import numpy as np
import random

class AgenteQL:
    def __init__(self, filas, columnas, acciones, tasa_aprendizaje=0.1, descuento=0.9, epsilon=1.0, epsilon_min=0.1, decaimiento=0.995):
        self.filas = filas
        self.columnas = columnas
        self.acciones = acciones
        self.q_table = np.zeros((filas, columnas, len(acciones)))

        self.alpha = tasa_aprendizaje
        self.gamma = descuento
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.decaimiento = decaimiento

    def elegir_accion(self, estado):
        if np.random.rand() < self.epsilon:
            return random.choice(self.acciones)  # Explorar
        fila, col = estado
        return np.argmax(self.q_table[fila][col])  # Explotar

    def actualizar(self, estado, accion, recompensa, siguiente_estado):
        fila, col = estado
        siguiente_fila, siguiente_col = siguiente_estado

        q_actual = self.q_table[fila][col][accion]
        q_max_siguiente = np.max(self.q_table[siguiente_fila][siguiente_col])

        # Actualizamos usando la fórmula de Q-learning
        nueva_q = q_actual + self.alpha * (recompensa + self.gamma * q_max_siguiente - q_actual)
        self.q_table[fila][col][accion] = nueva_q

    def reducir_exploracion(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.decaimiento

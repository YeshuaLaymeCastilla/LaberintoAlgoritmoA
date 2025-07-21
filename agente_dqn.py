import numpy as np
import random

class AgenteDQN:
    def __init__(self, filas, columnas, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.995, alpha=0.1, gamma=0.95):
        self.filas = filas
        self.columnas = columnas
        self.acciones = ["arriba", "abajo", "izquierda", "derecha"]
        self.q_table = {}
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.alpha = alpha
        self.gamma = gamma

    def obtener_q(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = np.zeros(len(self.acciones))
        return self.q_table[estado]

    def elegir_accion(self, estado):
        if random.random() < self.epsilon:
            return random.choice(self.acciones)
        else:
            q_values = self.obtener_q(estado)
            return self.acciones[np.argmax(q_values)]

    def actualizar(self, estado, accion, recompensa, nuevo_estado):
        q_actual = self.obtener_q(estado)
        q_nuevo = self.obtener_q(nuevo_estado)
        indice = self.acciones.index(accion)
        q_actual[indice] += self.alpha * (recompensa + self.gamma * np.max(q_nuevo) - q_actual[indice])

    def reducir_exploracion(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

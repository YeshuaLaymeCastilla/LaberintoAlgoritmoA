
import pygame
import sys
import matplotlib.pyplot as plt
import json
import random
from entorno import EntornoDQN
from agente_dqn import AgenteDQN
from astar import astar

pygame.init()

# 🟩 1. Pedir tamaño del laberinto
while True:
    try:
        dims = input("Tamaño del laberinto (Ej: 10x10): ").lower()
        filas, columnas = map(int, dims.split('x'))
        if filas > 1 and columnas > 1:
            break
    except:
        print("Formato inválido.")

# 🟩 2. Preguntar algoritmo
while True:
    metodo = input("¿Qué algoritmo deseas usar? (1=IA / 2=A*): ").strip()
    if metodo in ("1", "2"):
        metodo = int(metodo)
        break
    else:
        print("Solo se acepta 1 o 2.")

# Tamaño ventana
VENTANA_WIDTH, VENTANA_HEIGHT = 800, 800
TAM_CELDA = min(VENTANA_WIDTH // columnas, VENTANA_HEIGHT // filas)
ANCHO_VENTANA = TAM_CELDA * columnas
ALTO_VENTANA = TAM_CELDA * filas

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto - Selección de Algoritmo")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Inicializar mapa
laberinto = [[0 for _ in range(columnas)] for _ in range(filas)]
inicio = None
fin = None
modo = 1

# Dibujar
def dibujar_laberinto(camino=None):
    for fila in range(filas):
        for col in range(columnas):
            x = col * TAM_CELDA
            y = fila * TAM_CELDA
            color = BLANCO
            if laberinto[fila][col] == 1:
                color = NEGRO
            if (fila, col) == inicio:
                color = VERDE
            elif (fila, col) == fin:
                color = ROJO
            elif camino and (fila, col) in camino:
                color = AZUL
            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, (200, 200, 200), (x, y, TAM_CELDA, TAM_CELDA), 1)

    font = pygame.font.SysFont(None, 24)
    texto = font.render(f"Modo: {modo} | 1=Inicio, 2=Meta, 3=Obstáculo | Algoritmo: {'IA' if metodo == 1 else 'A*'}", True, (0, 0, 0))
    ventana.blit(texto, (10, 10))

# Editor visual
editando = True
pintando = False  # para detectar si el mouse está presionado
ultimo_modo = None  # recordar si se pinta o borra

while editando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                modo = 1
            elif evento.key == pygame.K_2:
                modo = 2
            elif evento.key == pygame.K_3:
                modo = 3
            elif evento.key == pygame.K_SPACE:
                if inicio and fin:
                    editando = False
                else:
                    print("Coloca inicio y fin antes de continuar.")

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = pygame.mouse.get_pos()
            fila = my // TAM_CELDA
            col = mx // TAM_CELDA
            if fila < filas and col < columnas:
                if modo == 1:
                    inicio = (fila, col)
                elif modo == 2:
                    fin = (fila, col)
                elif modo == 3:
                    if (fila, col) != inicio and (fila, col) != fin:
                        laberinto[fila][col] = 1 if laberinto[fila][col] == 0 else 0
                        ultimo_modo = laberinto[fila][col]
                        pintando = True

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            pintando = False
            ultimo_modo = None

        elif evento.type == pygame.MOUSEMOTION and pintando and modo == 3:
            mx, my = pygame.mouse.get_pos()
            fila = my // TAM_CELDA
            col = mx // TAM_CELDA
            if fila < filas and col < columnas and (fila, col) != inicio and (fila, col) != fin:
                laberinto[fila][col] = ultimo_modo

    ventana.fill(BLANCO)
    dibujar_laberinto()
    pygame.display.flip()

# 🟩 3. Ejecutar según el algoritmo
if metodo == 2:
    camino = astar(laberinto, inicio, fin)
    if camino:
        print("✅ Camino encontrado con A*.")
    else:
        print("❌ No se encontró camino con A*.")

    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                mostrando = False
        ventana.fill(BLANCO)
        dibujar_laberinto(camino)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

else:
    # IA (DQN)
    EPISODIOS = 3000
    entorno = EntornoDQN(laberinto, inicio, fin)
    agente = AgenteDQN(filas, columnas)
    recompensas = []

    for ep in range(EPISODIOS):
        estado = entorno.reset()
        terminado = False
        recompensa_total = 0
        pasos = 0
        max_pasos = filas * columnas

        while not terminado and pasos < max_pasos:
            accion = agente.elegir_accion(estado)
            nuevo_estado, recompensa, terminado = entorno.mover(accion)
            agente.actualizar(estado, accion, recompensa, nuevo_estado)
            estado = nuevo_state = nuevo_estado
            recompensa_total += recompensa
            pasos += 1

        recompensas.append(recompensa_total)
        agente.reducir_exploracion()

        if ep % 100 == 0:
            print(f"Episodio {ep}: Recompensa {recompensa_total}, Epsilon {agente.epsilon:.3f}")

    # Mostrar gráfico
    plt.plot(recompensas)
    plt.xlabel("Episodio")
    plt.ylabel("Recompensa")
    plt.title("Aprendizaje del Agente (DQN)")
    plt.show()
    pygame.quit()

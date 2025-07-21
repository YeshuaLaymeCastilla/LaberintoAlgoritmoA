import pygame
import sys
import random
import matplotlib.pyplot as plt
from entorno import Entorno
from agente import AgenteQL

# 🟩 1. Pedir tamaño del laberinto
while True:
    try:
        dims = input("Ingrese el tamaño del laberinto en formato FILAxCOLUMNA (ej: 10x10): ")
        filas, columnas = map(int, dims.lower().split('x'))
        if filas > 1 and columnas > 1:
            break
    except:
        print("Formato inválido. Intenta de nuevo.")

# 🟩 1.5 ¿Generar inicio/meta aleatorios?
usar_aleatorio = input("¿Deseas generar punto de partida y meta al azar? (S/N): ").strip().upper() == "S"

if usar_aleatorio:
    while True:
        inicio = (random.randint(0, filas-1), random.randint(0, columnas-1))
        fin = (random.randint(0, filas-1), random.randint(0, columnas-1))
        if inicio != fin:
            break
else:
    inicio = (0, 0)
    fin = (filas - 1, columnas - 1)

# 🟩 2. Calcular tamaño de celdas dinámicamente para que todo encaje en ventana
VENTANA_MAX = 800
TAM_CELDA = max(5, min(VENTANA_MAX // columnas, VENTANA_MAX // filas))
ANCHO_VENTANA = TAM_CELDA * columnas
ALTO_VENTANA = TAM_CELDA * filas

# 🟩 3. Inicializar laberinto
laberinto = [[0 for _ in range(columnas)] for _ in range(filas)]

# 🟩 4. Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)

# 🟩 5. Inicializar pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto - Editor y Entrenamiento IA")

# 🟩 6. Función de dibujo
def dibujar_laberinto(camino=None):
    for fila in range(filas):
        for col in range(columnas):
            x = col * TAM_CELDA
            y = fila * TAM_CELDA

            if laberinto[fila][col] == 1:
                color = NEGRO
            elif camino and (fila, col) in camino:
                color = AZUL
            else:
                color = BLANCO

            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, GRIS, (x, y, TAM_CELDA, TAM_CELDA), 1)

    pygame.draw.rect(ventana, VERDE, (inicio[1]*TAM_CELDA, inicio[0]*TAM_CELDA, TAM_CELDA, TAM_CELDA))
    pygame.draw.rect(ventana, ROJO, (fin[1]*TAM_CELDA, fin[0]*TAM_CELDA, TAM_CELDA, TAM_CELDA))

# 🟩 7. Editor de obstáculos (clic con trazo)
editando = True
mouse_presionado = False

while editando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Clic izquierdo
                mouse_presionado = True

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                mouse_presionado = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                editando = False  # inicia entrenamiento

    # Pintar con clic sostenido
    if mouse_presionado:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        fila = mouse_y // TAM_CELDA
        col = mouse_x // TAM_CELDA
        if 0 <= fila < filas and 0 <= col < columnas:
            if (fila, col) != inicio and (fila, col) != fin:
                laberinto[fila][col] = 1

    ventana.fill(BLANCO)
    dibujar_laberinto()
    pygame.display.flip()

# 🧠 ENTRENAMIENTO
entorno = Entorno(laberinto, inicio, fin)
acciones = entorno.acciones_posibles()
agente = AgenteQL(filas, columnas, acciones)

EPISODIOS = 10000
recompensas_por_ep = []

for ep in range(EPISODIOS):
    estado = entorno.reset()
    terminado = False
    recompensa_total = 0
    pasos = 0
    max_pasos = filas * columnas  # límite de pasos razonable

    while not terminado and pasos < max_pasos:
        accion = agente.elegir_accion(estado)
        nuevo_estado, recompensa, terminado = entorno.mover(accion)
        agente.actualizar(estado, accion, recompensa, nuevo_estado)
        estado = nuevo_estado
        recompensa_total += recompensa
        pasos += 1

    recompensas_por_ep.append(recompensa_total)
    agente.reducir_exploracion()

    if ep % 100 == 0:
        print(f"Episodio {ep} completado. Recompensa total: {recompensa_total}, Epsilon: {agente.epsilon:.3f}")

# 📊 Mostrar número de éxitos
exitos = sum([1 for r in recompensas_por_ep if r >= 100])
print(f"\nEpisodios con éxito (llegó a la meta): {exitos} de {EPISODIOS}")

# 📈 Mostrar gráfico de recompensas
plt.plot(recompensas_por_ep)
plt.title("Recompensa total por episodio")
plt.xlabel("Episodio")
plt.ylabel("Recompensa total")
plt.grid()
plt.show()

# 🔵 Visualización final del camino aprendido
estado = entorno.reset()
camino = [estado]
terminado = False

while not terminado:
    accion = agente.elegir_accion(estado)
    nuevo_estado, recompensa, terminado = entorno.mover(accion)
    camino.append(nuevo_estado)
    estado = nuevo_estado

mostrando = True
while mostrando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            mostrando = False

    ventana.fill(BLANCO)
    dibujar_laberinto(camino)
    pygame.display.flip()

pygame.quit()

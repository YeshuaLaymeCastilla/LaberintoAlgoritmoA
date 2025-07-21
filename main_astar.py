import pygame
import sys
from astar import a_star

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 120, 255)
GRIS = (220, 220, 220)

# Entrada de tamaño laberinto
while True:
    try:
        dims = input("Ingrese el tamaño del laberinto en formato FILAxCOLUMNA (ej: 10x15): ")
        filas, columnas = map(int, dims.lower().split("x"))
        if filas > 1 and columnas > 1:
            break
    except:
        print("Formato inválido. Intenta de nuevo.")

# Inicialización de pygame
pygame.init()
fuente = pygame.font.SysFont(None, 30)

TAM_CELDA = min(800 // columnas, 800 // filas)
ANCHO_VENTANA = TAM_CELDA * columnas
ALTO_VENTANA = TAM_CELDA * filas + 40  # 40px extra para texto

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto con algoritmo A*")

# Estados iniciales
laberinto = [[0 for _ in range(columnas)] for _ in range(filas)]
inicio = None
fin = None
camino = []
modo = 1  # 1: inicio, 2: meta, 3: obstáculos
pintando = False
ultimo_modo = 1

def dibujar_laberinto():
    # Texto arriba
    modos = {1: "INICIO (1)", 2: "META (2)", 3: "OBSTÁCULOS (3)"}
    texto = fuente.render(f"Modo: {modos.get(modo, '')}", True, (0, 0, 0))
    ventana.fill(GRIS, (0, 0, ANCHO_VENTANA, 40))
    ventana.blit(texto, (10, 10))

    for fila in range(filas):
        for col in range(columnas):
            color = BLANCO
            if laberinto[fila][col] == 1:
                color = NEGRO
            if (fila, col) == inicio:
                color = VERDE
            elif (fila, col) == fin:
                color = ROJO
            elif (fila, col) in camino:
                color = AZUL

            x = col * TAM_CELDA
            y = fila * TAM_CELDA + 40
            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, (200, 200, 200), (x, y, TAM_CELDA, TAM_CELDA), 1)

# Loop principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
            break

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                modo = 1
            elif evento.key == pygame.K_2:
                modo = 2
            elif evento.key == pygame.K_3:
                modo = 3
            elif evento.key == pygame.K_r:
                laberinto = [[0 for _ in range(columnas)] for _ in range(filas)]
                inicio = None
                fin = None
                camino = []
                modo = 1
                print("Laberinto reiniciado.")
            elif evento.key == pygame.K_SPACE:
                if inicio and fin:
                    camino = a_star(laberinto, inicio, fin)
                    if camino:
                        print("Camino encontrado!")
                    else:
                        print("No hay camino disponible.")
                else:
                    print("Define inicio y meta primero (teclas 1 y 2).")

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = pygame.mouse.get_pos()
            if my >= 40:
                fila = (my - 40) // TAM_CELDA
                col = mx // TAM_CELDA
                if 0 <= fila < filas and 0 <= col < columnas:
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

        elif evento.type == pygame.MOUSEMOTION and pintando and modo == 3:
            mx, my = pygame.mouse.get_pos()
            if my >= 40:
                fila = (my - 40) // TAM_CELDA
                col = mx // TAM_CELDA
                if 0 <= fila < filas and 0 <= col < columnas:
                    if (fila, col) != inicio and (fila, col) != fin:
                        laberinto[fila][col] = ultimo_modo

    dibujar_laberinto()
    pygame.display.flip()

pygame.quit()
sys.exit()

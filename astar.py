import heapq

def a_star(laberinto, inicio, fin):
    filas = len(laberinto)
    columnas = len(laberinto[0])

    def heuristica(a, b):
        # Distancia Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    abiertos = []
    heapq.heappush(abiertos, (0 + heuristica(inicio, fin), 0, inicio))
    came_from = {}
    costo_actual = {inicio: 0}

    while abiertos:
        _, costo, actual = heapq.heappop(abiertos)

        if actual == fin:
            # Reconstruir camino
            camino = []
            while actual in came_from:
                camino.append(actual)
                actual = came_from[actual]
            camino.append(inicio)
            camino.reverse()
            return camino

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            vecino = (actual[0] + dx, actual[1] + dy)

            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                if laberinto[vecino[0]][vecino[1]] == 1:
                    continue  # obstáculo

                nuevo_costo = costo_actual[actual] + 1
                if vecino not in costo_actual or nuevo_costo < costo_actual[vecino]:
                    costo_actual[vecino] = nuevo_costo
                    prioridad = nuevo_costo + heuristica(vecino, fin)
                    heapq.heappush(abiertos, (prioridad, nuevo_costo, vecino))
                    came_from[vecino] = actual

    return []  # No hay camino

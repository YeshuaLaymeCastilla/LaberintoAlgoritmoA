# LaberintoAlgoritmoA

Implementación del algoritmo A estrella (A*) en Python para resolver laberintos representados por matrices. Se utiliza la heurística Manhattan y una cola de prioridad (heapq) para encontrar el camino más corto. Este proyecto incluye una visualización opcional con pygame.

# Cómo ejecutar el proyecto
La parte principal del proyecto está contenida en los archivos:

main_astar.py

astar.py

# Para ejecutar el algoritmo A* y ver el laberinto resuelto:
"python main_astar.py"

Esto ejecutará el sistema de búsqueda y mostrará la salida según la configuración interna del laberinto.

# Archivos del proyecto
main_astar.py → Punto de entrada principal para ejecutar el algoritmo A*.

astar.py → Implementación del algoritmo A estrella.

main.py, main_dqn.py, agente.py, agente_dqn.py, entorno.py → Archivos de pruebas y versiones experimentales con modelos de inteligencia artificial progresiva. Se incluyeron como parte del proceso de exploración, pero no son necesarios para ejecutar la versión principal.


# Requisitos
Python 3.8 o superior
(Opcional) pygame para visualización

# Instalación recomendada:
pip install pygame

# Características
Resolución de laberintos ortogonales (sin diagonales).
Heurística Manhattan (admisible y eficiente).
Estructura clara y modular.
Código listo para extensión futura con IA o visualización.

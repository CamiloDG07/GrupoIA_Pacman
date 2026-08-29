"""
Actividad 1 - Exploracion del entorno
======================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 1.

Este script NO implementa ningun algoritmo (search.py y searchAgents.py
todavia no se tocan en esta actividad). Su unico proposito es responder,
de forma reproducible y con evidencia de codigo real, la pregunta de
analisis de la guia:

    "Identifique los componentes del problema de busqueda dentro del
     entorno Pac-Man."

Para eso instanciamos el mismo PositionSearchProblem que usa el propio
SearchAgent del proyecto (searchAgents.py, ya provisto) y mostramos,
en vivo, cada componente P = (S, A, T, s0, G, C) descrito en la guia.

Ejecucion:
    python experimentos/actividad1_exploracion.py [layout]

Por defecto usa el layout "tinyMaze" (el mismo de la guia).
"""
import sys

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import PositionSearchProblem


def explorar(layout_name="tinyMaze"):
    lay = layout_module.getLayout(layout_name)
    if lay is None:
        raise SystemExit(f"No se encontro el layout '{layout_name}' en pacman/layouts/")

    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)

    # PositionSearchProblem es el SearchProblem por defecto que usa
    # SearchAgent (searchAgents.py, lineas ~120-210). Por defecto su
    # objetivo es la posicion (1, 1).
    problem = PositionSearchProblem(state)

    print("=" * 70)
    print(f"Actividad 1 - Componentes del problema de busqueda ({layout_name})")
    print("=" * 70)

    s0 = problem.getStartState()
    print(f"\n[S]  Estado (s):        posicion (x, y) de Pac-Man en el laberinto")
    print(f"[s0] Estado inicial:    {s0}")

    print(f"\n[A]  Acciones disponibles en s0:")
    sucesores = problem.getSuccessors(s0)
    for successor, action, stepCost in sucesores:
        print(f"     accion={action:6s} -> sucesor={successor}  costo_paso={stepCost}")
    if not sucesores:
        print("     (sin sucesores: revisar layout)")

    print(f"\n[T]  Funcion de transicion / sucesor: getSuccessors(state) -> "
          f"{len(sucesores)} sucesores desde s0 en este layout")

    print(f"\n[G]  Prueba de objetivo isGoalState(s0) = {problem.isGoalState(s0)}")
    print(f"     Objetivo configurado en este problema: problem.goal = {problem.goal}")

    print(f"\n[C]  Costo: cada movimiento legal cuesta 1 "
          f"(ver PositionSearchProblem.costFn, por defecto lambda x: 1)")

    print(f"\nDimensiones del laberinto: {lay.width} x {lay.height}"
          f"  |  Paredes totales: {lay.walls.count()}"
          f"  |  Alimentos totales: {lay.food.count()}")

    print("\nResumen para la tabla de la guia:")
    tabla = [
        ("Estado", "Posicion (x, y) de Pac-Man dentro del laberinto."),
        ("Estado inicial", f"{s0} (posicion de partida en '{layout_name}')."),
        ("Acciones", "North, South, East, West; solo si no hay pared en esa direccion."),
        ("Funcion sucesor", "getSuccessors(state): devuelve (sucesor, accion, costo) por cada movimiento legal."),
        ("Objetivo", f"isGoalState(state); en PositionSearchProblem, llegar a {problem.goal}."),
        ("Costo", "1 por movimiento (suma de pasos = longitud del camino)."),
    ]
    for elemento, descripcion in tabla:
        print(f"  - {elemento}: {descripcion}")


if __name__ == "__main__":
    layout_arg = sys.argv[1] if len(sys.argv) > 1 else "tinyMaze"
    explorar(layout_arg)

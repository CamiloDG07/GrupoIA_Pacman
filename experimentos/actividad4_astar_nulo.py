"""
Actividad 4 - A* sin informacion (h(n) = 0)
=============================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 4.

Formaliza, sobre el layout de referencia (mediumClassic, ver nota en la
Actividad 2/3 sobre por que se abandono mediumMaze), la comparacion entre:

  - UCS (Actividad 2)
  - A* + nullHeuristic, es decir h(n) = 0 (Actividad 3)

y guarda ambas filas en resultados/resultados.csv bajo actividad=4, para la
tabla que pide la guia: Algoritmo, Costo, Expandidos, Tiempo.

Ejecucion:
    python experimentos/actividad4_astar_nulo.py [layout]
"""
import sys
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import PositionSearchProblem
from search import uniformCostSearch, aStarSearch, nullHeuristic

from _resultados import guardar_fila

LAYOUT_POR_DEFECTO = "mediumClassic"


def _medir(layout_name, nombre, funcion):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = PositionSearchProblem(state, warn=False)

    inicio = time.perf_counter()
    acciones = funcion(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded

    guardar_fila({
        "actividad": "4",
        "metodo_heuristica": nombre,
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
    })
    return costo, len(acciones), expandidos, tiempo


def comparar(layout_name):
    print("=" * 70)
    print(f"Actividad 4 - A* con h(n)=0 vs. UCS sobre '{layout_name}'")
    print("=" * 70)

    resultados = {
        "UCS": _medir(layout_name, "UCS", uniformCostSearch),
        "A* + h(n)=0": _medir(layout_name, "A*+h=0", lambda p: aStarSearch(p, nullHeuristic)),
    }

    print(f"\n{'Algoritmo':15s} {'Costo':>6s} {'Expandidos':>11s} {'Tiempo (s)':>12s}")
    for nombre, (costo, longitud, expandidos, tiempo) in resultados.items():
        print(f"{nombre:15s} {costo:6d} {expandidos:11d} {tiempo:12.6f}")

    costo_ucs = resultados["UCS"][0]
    exp_ucs = resultados["UCS"][2]
    costo_astar = resultados["A* + h(n)=0"][0]
    exp_astar = resultados["A* + h(n)=0"][2]

    print("\nVerificacion:")
    print(f"  Mismo costo (ambas optimas): {costo_ucs == costo_astar}")
    print(f"  Mismos nodos expandidos:     {exp_ucs == exp_astar}")
    print("\nFilas guardadas en resultados/resultados.csv (actividad=4).")


if __name__ == "__main__":
    layout_arg = sys.argv[1] if len(sys.argv) > 1 else LAYOUT_POR_DEFECTO
    comparar(layout_arg)

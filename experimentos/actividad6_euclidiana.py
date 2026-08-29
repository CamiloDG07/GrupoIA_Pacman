"""
Actividad 6 - Distancia Euclidiana y comparacion de heuristicas
==================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 6.

euclideanHeuristic YA esta provista por el proyecto en searchAgents.py (no
hay que implementarla). Esta actividad ejecuta A* con heuristica nula,
Manhattan y Euclidiana sobre el layout de referencia (mediumClassic) y las
compara entre si (la tabla de la guia pide Heuristica/Longitud/Costo/
Expandidos/Tiempo).

Ejecucion:
    python experimentos/actividad6_euclidiana.py [layout]
"""
import sys
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import PositionSearchProblem, manhattanHeuristic, euclideanHeuristic
from search import aStarSearch, nullHeuristic

from _resultados import guardar_fila

LAYOUT_POR_DEFECTO = "mediumClassic"


def _medir(layout_name, nombre, heuristica):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = PositionSearchProblem(state, warn=False)

    inicio = time.perf_counter()
    acciones = aStarSearch(problem, heuristica)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded

    guardar_fila({
        "actividad": "6",
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
    print("=" * 78)
    print(f"Actividad 6 - Comparacion de heuristicas (A*) sobre '{layout_name}'")
    print("=" * 78)

    heuristicas = {
        "h(n)=0": nullHeuristic,
        "Manhattan": manhattanHeuristic,
        "Euclidiana": euclideanHeuristic,
    }

    resultados = {nombre: _medir(layout_name, nombre, h) for nombre, h in heuristicas.items()}

    print(f"\n{'Heuristica':12s} {'Longitud':>9s} {'Costo':>6s} {'Expandidos':>11s} {'Tiempo (s)':>12s}")
    for nombre, (costo, longitud, expandidos, tiempo) in resultados.items():
        print(f"{nombre:12s} {longitud:9d} {costo:6d} {expandidos:11d} {tiempo:12.6f}")

    exp_null = resultados["h(n)=0"][2]
    exp_man = resultados["Manhattan"][2]
    exp_euc = resultados["Euclidiana"][2]

    print(f"\nManhattan expande {exp_null - exp_man} nodos menos que h(n)=0 "
          f"({exp_null} -> {exp_man}).")
    print(f"Euclidiana expande {exp_null - exp_euc} nodos menos que h(n)=0 "
          f"({exp_null} -> {exp_euc}).")
    print(f"Manhattan vs. Euclidiana: {exp_man} vs. {exp_euc} nodos expandidos "
          f"({'Manhattan es mas informativa' if exp_man < exp_euc else 'Euclidiana es mas informativa' if exp_euc < exp_man else 'empate'} "
          f"en este layout).")

    print("\nFilas guardadas en resultados/resultados.csv (actividad=6).")


if __name__ == "__main__":
    layout_arg = sys.argv[1] if len(sys.argv) > 1 else LAYOUT_POR_DEFECTO
    comparar(layout_arg)

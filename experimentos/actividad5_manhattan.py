"""
Actividad 5 - A* con distancia Manhattan
===========================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 5.

manhattanHeuristic YA esta provista por el proyecto en searchAgents.py (no
hay que implementarla); esta actividad es ejecutar A* con ella sobre el
layout de referencia (mediumClassic) y compararla contra UCS.

Ejecucion:
    python experimentos/actividad5_manhattan.py [layout]
"""
import sys
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import PositionSearchProblem, manhattanHeuristic
from search import uniformCostSearch, aStarSearch

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
    # _visitedlist: celdas efectivamente expandidas, en el orden en que se
    # expandieron. Es lo mismo que graphicsDisplay.py usa para "pintar" las
    # celdas exploradas cuando se corre con interfaz grafica (aqui no hay
    # pantalla, pero es la misma informacion que se "observaria graficamente").
    celdas_exploradas = list(problem._visitedlist)

    guardar_fila({
        "actividad": "5",
        "metodo_heuristica": nombre,
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
    })
    return costo, len(acciones), expandidos, tiempo, celdas_exploradas


def comparar(layout_name):
    print("=" * 70)
    print(f"Actividad 5 - A* con distancia Manhattan vs. UCS sobre '{layout_name}'")
    print("=" * 70)

    resultados = {
        "UCS": _medir(layout_name, "UCS", uniformCostSearch),
        "A* + Manhattan": _medir(layout_name, "A*+Manhattan",
                                  lambda p: aStarSearch(p, manhattanHeuristic)),
    }

    print(f"\n{'Algoritmo':16s} {'Costo':>6s} {'Expandidos':>11s} {'Tiempo (s)':>12s}")
    for nombre, (costo, longitud, expandidos, tiempo, _) in resultados.items():
        print(f"{nombre:16s} {costo:6d} {expandidos:11d} {tiempo:12.6f}")

    exp_ucs = resultados["UCS"][2]
    exp_man = resultados["A* + Manhattan"][2]
    celdas_ucs = set(resultados["UCS"][4])
    celdas_man = set(resultados["A* + Manhattan"][4])

    print(f"\nReduccion de nodos expandidos: UCS={exp_ucs} -> A*+Manhattan={exp_man} "
          f"(R = {exp_ucs / exp_man:.2f}x menos expansiones)")
    print(f"Celdas exploradas por UCS pero NO por A*+Manhattan: "
          f"{len(celdas_ucs - celdas_man)} de {len(celdas_ucs)}")

    print("\nFilas guardadas en resultados/resultados.csv (actividad=5).")


if __name__ == "__main__":
    layout_arg = sys.argv[1] if len(sys.argv) > 1 else LAYOUT_POR_DEFECTO
    comparar(layout_arg)

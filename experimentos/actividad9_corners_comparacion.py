"""
Actividad 9 - Experimento comparativo sobre CornersProblem
==================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 9.

Corre las cuatro estrategias que pide la guia sobre tinyCorners (UCS,
A*+h=0, A*+heuristica basica, A*+heuristica propuesta), arma la tabla
Metodo/Costo/Expandidos/Tiempo/Optimo y calcula el factor de reduccion de
expansiones:

    R = N_UCS / N_A*

usando la heuristica propuesta (la mas informada, la que usa
AStarCornersAgent) como N_A* de referencia.

Ejecucion:
    python experimentos/actividad9_corners_comparacion.py
"""
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import CornersProblem, cornersHeuristicBasica, cornersHeuristic
from search import uniformCostSearch, aStarSearch, nullHeuristic

from _resultados import guardar_fila

LAYOUT_PRINCIPAL = "tinyCorners"


def _nuevo_problema(layout_name):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    return CornersProblem(state)


def _medir(layout_name, metodo, funcion_busqueda, costo_optimo_referencia):
    problem = _nuevo_problema(layout_name)

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    optimo = "si" if costo == costo_optimo_referencia else "no"

    guardar_fila({
        "actividad": "9",
        "metodo_heuristica": metodo,
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": optimo,
    })
    return costo, len(acciones), expandidos, tiempo, optimo


def experimento_comparativo(layout_name):
    print("=" * 88)
    print(f"Actividad 9 - Experimento comparativo sobre '{layout_name}'")
    print("=" * 88)

    # Primero UCS, que fija el costo optimo de referencia para juzgar
    # "optimo" en las demas filas. UCS es optimo por definicion, asi que se
    # usa su propio costo como referencia (comparar consigo mismo siempre da
    # "si").
    problem_ucs = _nuevo_problema(layout_name)
    inicio = time.perf_counter()
    acciones_ucs = uniformCostSearch(problem_ucs)
    t_ucs = time.perf_counter() - inicio
    costo_ucs = problem_ucs.getCostOfActions(acciones_ucs)
    long_ucs = len(acciones_ucs)
    exp_ucs = problem_ucs._expanded
    guardar_fila({
        "actividad": "9", "metodo_heuristica": "UCS", "layout": layout_name,
        "costo": costo_ucs, "longitud_camino": long_ucs, "nodos_expandidos": exp_ucs,
        "tiempo_seg": f"{t_ucs:.6f}", "optimo": "si",
    })

    metodos = {
        "A* + h=0": lambda p: aStarSearch(p, nullHeuristic),
        "A* + heuristica basica": lambda p: aStarSearch(p, cornersHeuristicBasica),
        "A* + heuristica propuesta": lambda p: aStarSearch(p, cornersHeuristic),
    }

    filas = {"UCS": (costo_ucs, long_ucs, exp_ucs, t_ucs, "si")}
    for nombre, f in metodos.items():
        filas[nombre] = _medir(layout_name, nombre, f, costo_optimo_referencia=costo_ucs)

    print(f"{'Metodo':26s} {'Costo':>6s} {'Expandidos':>11s} {'Tiempo (s)':>12s} {'Optimo':>7s}")
    for nombre, (costo, longitud, expandidos, tiempo, optimo) in filas.items():
        print(f"{nombre:26s} {costo:6d} {expandidos:11d} {tiempo:12.6f} {optimo:>7s}")

    for nombre, (costo, _, _, _, optimo) in filas.items():
        assert optimo == "si", f"{nombre} no alcanzo el costo optimo ({costo} != {costo_ucs})"

    n_ucs = filas["UCS"][2]
    n_astar_propuesta = filas["A* + heuristica propuesta"][2]
    R = n_ucs / n_astar_propuesta
    print()
    print(f"Factor de reduccion R = N_UCS / N_A* = {n_ucs} / {n_astar_propuesta} = {R:.2f}")
    print(f"(usando la heuristica propuesta, la mas informada, como referencia de N_A*)")
    print(f"UCS expandio aproximadamente {R:.2f} veces mas estados que A*+heuristica propuesta.")
    print()


if __name__ == "__main__":
    experimento_comparativo(LAYOUT_PRINCIPAL)
    print("Filas guardadas en resultados/resultados.csv (actividad=9).")

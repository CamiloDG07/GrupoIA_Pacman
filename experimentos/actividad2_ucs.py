"""
Actividad 2 - Busqueda de costo uniforme (UCS)
================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 2.

Este script mide el algoritmo `uniformCostSearch` ya implementado en
pacman/search.py (Actividad 2). NO reimplementa el algoritmo: solo lo llama
y registra sus metricas, para dejar una linea base con la que se comparara
A* en las Actividades 4, 6 y 9.

Nota sobre `python pacman.py -l <layout> -p SearchAgent -a fn=ucs`:
------------------------------------------------------------------
Correr ese comando reproduce exactamente el mismo costo/nodos/tiempo que
imprime este script (se llama al mismo `uniformCostSearch`), pero en los
layouts de este proyecto (que traen muchos alimentos, no solo el necesario
para el problema de posicion) el proceso termina con
`Exception: Illegal action Stop` DESPUES de imprimir los resultados. Esto
ocurre porque, una vez que Pac-Man agota el plan encontrado, SearchAgent
(que la guia pide no modificar) devuelve Directions.STOP, y en este motor
STOP nunca es una accion legal para Pac-Man (ver PacmanRules.getLegalActions
en pacman.py). No afecta la busqueda ni las metricas: estas ya se calcularon
y se imprimieron dentro de `registerInitialState`, antes de que ocurra el
error. Por eso este script mide directamente sobre el SearchProblem, sin
pasar por el bucle de juego completo.

Ejecucion:
    python experimentos/actividad2_ucs.py [layout]
"""
import sys
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import PositionSearchProblem
from search import uniformCostSearch

from _resultados import guardar_fila

LAYOUT_POR_DEFECTO = "mediumMaze"


def correr_ucs(layout_name):
    lay = layout_module.getLayout(layout_name)
    if lay is None:
        raise SystemExit(f"No se encontro el layout '{layout_name}' en pacman/layouts/")

    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = PositionSearchProblem(state, warn=False)

    inicio = time.perf_counter()
    acciones = uniformCostSearch(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    longitud = len(acciones)
    expandidos = problem._expanded

    print("=" * 70)
    print(f"Actividad 2 - UCS sobre '{layout_name}'")
    print("=" * 70)
    print(f"Estado inicial:     {problem.getStartState()}")
    print(f"Objetivo:           {problem.goal}")
    print(f"Costo del camino:   {costo}")
    print(f"Longitud del camino:{longitud}")
    print(f"Nodos expandidos:   {expandidos}")
    print(f"Tiempo:             {tiempo:.6f} s")

    guardar_fila({
        "actividad": "2",
        "metodo_heuristica": "UCS",
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": longitud,
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
    })
    print(f"\nFila guardada en resultados/resultados.csv "
          f"(actividad=2, metodo=UCS, layout={layout_name}).")
    return costo, longitud, expandidos, tiempo


if __name__ == "__main__":
    layout_arg = sys.argv[1] if len(sys.argv) > 1 else LAYOUT_POR_DEFECTO
    correr_ucs(layout_arg)

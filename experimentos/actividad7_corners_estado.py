"""
Actividad 7 - Diseno del estado para CornersProblem
==================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 7.

Se completaron getStartState, isGoalState y getSuccessors de CornersProblem
en searchAgents.py. El estado elegido es:

    s = (posicion, esquinas_visitadas)

donde "esquinas_visitadas" es una tupla de 4 booleanos (uno por esquina de
self.corners, en el mismo orden). Este script corre UCS sobre tinyCorners
(y confirma, independientemente, que mediumCorners no es utilizable en esta
copia del proyecto: el punto de partida de Pac-Man queda en un cuarto
completamente sellado sin salida -- ver el hallazgo documentado en el
informe).

Ejecucion:
    python experimentos/actividad7_corners_estado.py
"""
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import CornersProblem, PositionSearchProblem
from search import uniformCostSearch

from _resultados import guardar_fila

LAYOUT_PRINCIPAL = "tinyCorners"


def probar_conectividad_mediumCorners():
    """
    Verifica, usando PositionSearchProblem (ya implementado por el
    profesor, sin tocar), que el punto de partida de mediumCorners no
    puede llegar ni siquiera a UNA esquina -- confirma que el problema es
    del layout, no de nuestra implementacion de CornersProblem.
    """
    lay = layout_module.getLayout("mediumCorners")
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = PositionSearchProblem(state, goal=(1, 1), warn=False)
    acciones = uniformCostSearch(problem)
    alcanzable = len(acciones) > 0 or problem.isGoalState(problem.getStartState())
    print(f"Verificacion mediumCorners: (1,1) alcanzable desde el inicio = {alcanzable}")
    if not alcanzable:
        print("  -> Confirmado con PositionSearchProblem (codigo del profesor, sin tocar):")
        print("     el punto de partida de mediumCorners esta en un cuarto sellado.")
        print("     mediumCorners NO se usa como layout de referencia por este motivo.")
    return alcanzable


def probar_corners(layout_name):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = CornersProblem(state)

    print(f"Layout: {layout_name}")
    print(f"  Esquinas: {problem.corners}")
    print(f"  Estado inicial: {problem.getStartState()}")

    inicio = time.perf_counter()
    acciones = uniformCostSearch(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded

    guardar_fila({
        "actividad": "7",
        "metodo_heuristica": "UCS",
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
    })

    print(f"  UCS: costo={costo} longitud={len(acciones)} expandidos={expandidos} tiempo={tiempo:.6f}s")
    print()
    return costo, len(acciones), expandidos, tiempo


if __name__ == "__main__":
    probar_conectividad_mediumCorners()
    print()
    probar_corners(LAYOUT_PRINCIPAL)
    print("Filas guardadas en resultados/resultados.csv (actividad=7).")

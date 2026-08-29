"""
Actividad 3 - Implementacion de A* (verificacion de correctitud)
==================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 3.

La guia no pide una tabla de resultados para esta actividad (esa llega en
la Actividad 4 en adelante): pide implementar `aStarSearch` cumpliendo 8
requisitos puntuales. Este script no es el entregable de la actividad (eso
es el codigo en pacman/search.py); es la evidencia de que la implementacion
cumple lo pedido, comparando A* contra la linea base de UCS (Actividad 2)
en varios layouts:

  1) A* con heuristica nula debe dar EXACTAMENTE el mismo costo y el mismo
     numero de nodos expandidos que UCS (Actividad 4 lo explica formalmente).
  2) A* con Manhattan/Euclidiana debe seguir encontrando el costo OPTIMO
     (el mismo que UCS), pero puede expandir menos (o igual) nodos.

De paso, este script fue el que nos hizo notar que 'mediumMaze' es un
pasillo casi sin bifurcaciones: ninguna heuristica reduce alli los nodos
expandidos frente a h(n)=0, simplemente porque no hay bifurcaciones donde
"elegir mejor" cambie algo. Por eso a partir de esta actividad se usa
'mediumClassic' (con bifurcaciones reales) como layout principal de
comparacion para las Actividades 4, 5, 6 y 9; 'mediumMaze' se conserva solo
como caso de contraste (heuristicas "inutiles" en un pasillo).

Ejecucion:
    python experimentos/actividad3_astar_verificacion.py
"""
from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
import search
from searchAgents import PositionSearchProblem, manhattanHeuristic, euclideanHeuristic

LAYOUTS = ["tinyMaze", "mediumMaze", "mediumClassic", "openClassic", "trickyClassic"]


def _correr(layout_name, funcion, heuristica=None):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = PositionSearchProblem(state, warn=False)
    acciones = funcion(problem, heuristica) if heuristica is not None else funcion(problem)
    return problem.getCostOfActions(acciones), problem._expanded


def verificar():
    print("=" * 88)
    print("Actividad 3 - Verificacion de aStarSearch contra la linea base de UCS")
    print("=" * 88)
    fallas = []
    for layout_name in LAYOUTS:
        costo_ucs, exp_ucs = _correr(layout_name, search.uniformCostSearch)
        costo_h0, exp_h0 = _correr(layout_name, search.aStarSearch, search.nullHeuristic)
        costo_man, exp_man = _correr(layout_name, search.aStarSearch, manhattanHeuristic)
        costo_euc, exp_euc = _correr(layout_name, search.aStarSearch, euclideanHeuristic)

        print(f"\n{layout_name}:")
        print(f"  UCS             costo={costo_ucs:4d}  expandidos={exp_ucs:4d}")
        print(f"  A* + h=0        costo={costo_h0:4d}  expandidos={exp_h0:4d}")
        print(f"  A* + Manhattan  costo={costo_man:4d}  expandidos={exp_man:4d}")
        print(f"  A* + Euclidiana costo={costo_euc:4d}  expandidos={exp_euc:4d}")

        if not (costo_ucs == costo_h0 == costo_man == costo_euc):
            fallas.append(f"{layout_name}: los costos deberian coincidir (todas optimas)")
        if exp_ucs != exp_h0:
            fallas.append(f"{layout_name}: A*+h=0 deberia expandir igual que UCS")
        if exp_man > exp_h0 or exp_euc > exp_h0:
            fallas.append(f"{layout_name}: una heuristica admisible no deberia expandir mas que h=0")

    print("\n" + "=" * 88)
    if fallas:
        print("FALLAS DETECTADAS:")
        for f in fallas:
            print(f"  - {f}")
        raise SystemExit(1)
    print("Todas las verificaciones pasaron: A* es correcto y consistente con UCS.")


if __name__ == "__main__":
    verificar()

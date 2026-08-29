"""
Actividad 10 - Busqueda de todos los alimentos (FoodSearchProblem)
====================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 10.

FoodSearchProblem YA esta completamente implementado por el profesor en
searchAgents.py (getStartState, isGoalState, getSuccessors, getCostOfActions).
No hay codigo que escribir en esta actividad: el objetivo es entender el
problema (estado = (posicion, foodGrid), meta cuando foodGrid.count()==0) y
establecer una linea base (UCS y A*+h(n)=0, que deben coincidir exactamente,
igual que en la Actividad 4) antes de disenar heuristicas en la Actividad 11.

Se corre sobre dos layouts pequenos (tinySearch: 1 alimento; testClassic:
8 alimentos) porque el espacio de estados de este problema crece de forma
exponencial en el numero de alimentos F (hasta 2^F configuraciones posibles
de "alimento presente/consumido"): un layout con muchos alimentos (ver la
seccion de "Analisis" al final de este script) se vuelve intratable para UCS
puro sin ninguna heuristica que lo guie.

Ejecucion:
    python experimentos/actividad10_food_baseline.py
"""
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import FoodSearchProblem
from search import uniformCostSearch, aStarSearch, nullHeuristic

from _resultados import guardar_fila

LAYOUTS = ["tinySearch", "testClassic"]


def _medir(layout_name, nombre, funcion_busqueda):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = FoodSearchProblem(state)

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    numFoodInicial = state.getFood().count()

    guardar_fila({
        "actividad": "10",
        "metodo_heuristica": nombre,
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
    })
    return costo, len(acciones), expandidos, tiempo, numFoodInicial


def explorar(layout_name):
    print("=" * 78)
    print(f"Actividad 10 - FoodSearchProblem sobre '{layout_name}'")
    print("=" * 78)

    costo_u, long_u, exp_u, t_u, nfood = _medir(layout_name, "UCS", uniformCostSearch)
    costo_a, long_a, exp_a, t_a, _ = _medir(
        layout_name, "A*+h(n)=0", lambda p: aStarSearch(p, nullHeuristic)
    )

    print(f"Alimentos iniciales en el layout: {nfood}")
    print(f"{'Metodo':12s} {'Costo':>6s} {'Longitud':>9s} {'Expandidos':>11s} {'Tiempo (s)':>12s}")
    print(f"{'UCS':12s} {costo_u:6d} {long_u:9d} {exp_u:11d} {t_u:12.6f}")
    print(f"{'A*+h(n)=0':12s} {costo_a:6d} {long_a:9d} {exp_a:11d} {t_a:12.6f}")

    assert costo_u == costo_a, "UCS y A*+h=0 deberian encontrar el mismo costo optimo"
    assert exp_u == exp_a, "Con h(n)=0, A* deberia expandir exactamente lo mismo que UCS"
    print("Verificado: mismo costo optimo y mismos nodos expandidos (igual que en la Actividad 4).")
    print()


if __name__ == "__main__":
    for layout_name in LAYOUTS:
        explorar(layout_name)

    print("=" * 78)
    print("Nota sobre crecimiento del espacio de estados (no incluido en resultados.csv):")
    print("Se intento correr UCS sobre 'smallClassic' (55 alimentos) con un limite de 45s")
    print("y NO termino: es la explosion combinatoria 2^F que menciona la guia (con F=55,")
    print("2^55 configuraciones posibles de alimento presente/consumido). Por eso los")
    print("layouts de esta actividad y de la 11 se restringen a testClassic (8 alimentos)")
    print("y tinySearch (1 alimento), donde UCS puro SI es viable como linea base.")
    print("Filas guardadas en resultados/resultados.csv (actividad=10).")

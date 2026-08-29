"""
Actividad 11 - Diseno de foodHeuristic (dos versiones + cache)
==================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 11.

Se implementaron dos heuristicas para FoodSearchProblem en searchAgents.py:

  Heuristica 1 (foodHeuristicV1): la formula que sugiere la guia como
  primera aproximacion, la distancia Manhattan al alimento mas lejano:
      h(n) = max_{f en F} d_M(n, f)

  Heuristica 2 (foodHeuristic, la que usa AStarFoodSearchAgent): el
  diametro Manhattan del conjunto {posicion actual} U {alimentos
  restantes} -- generaliza la Heuristica 1 considerando tambien la
  distancia entre pares de alimentos, no solo la distancia desde Pac-Man.
  Usa problem.heuristicInfo para cachear, una sola vez, la distancia
  Manhattan entre cada par de alimentos del layout inicial.

Este script hace dos cosas:
  1. Reproduce la tabla que pide la guia (h(n)=0 / Heuristica 1 /
     Heuristica 2) sobre tinySearch y testClassic, verificando que las
     tres encuentran el mismo costo optimo y que ninguna heuristica
     expande mas nodos que h(n)=0.
  2. El "Reto" de cache: compara el tiempo de A*+Heuristica 2 CON cache
     (foodHeuristic) contra una version SIN cache (foodHeuristicV2SinCache,
     misma formula pero recalculando las distancias entre pares de comida
     en cada llamada) sobre testClassic y capsuleClassic.

Ejecucion:
    python experimentos/actividad11_food_heuristic.py
"""
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import (
    FoodSearchProblem,
    foodHeuristicV1,
    foodHeuristic,
    foodHeuristicV2SinCache,
)
from search import aStarSearch, nullHeuristic

from _resultados import guardar_fila

LAYOUTS_COMPARACION = ["tinySearch", "testClassic"]
LAYOUTS_CACHE = ["testClassic", "capsuleClassic"]
REPETICIONES_CACHE = 5


def _medir(layout_name, nombre, funcion_busqueda, guardar=True):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    problem = FoodSearchProblem(state)

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded

    if guardar:
        guardar_fila({
            "actividad": "11",
            "metodo_heuristica": nombre,
            "layout": layout_name,
            "costo": costo,
            "longitud_camino": len(acciones),
            "nodos_expandidos": expandidos,
            "tiempo_seg": f"{tiempo:.6f}",
            "optimo": "si",
        })
    return costo, len(acciones), expandidos, tiempo


def comparar_heuristicas(layout_name):
    print("=" * 78)
    print(f"Actividad 11 - Comparacion de heuristicas de comida sobre '{layout_name}'")
    print("=" * 78)

    heuristicas = {
        "h(n)=0": lambda p: aStarSearch(p, nullHeuristic),
        "Heuristica 1": lambda p: aStarSearch(p, foodHeuristicV1),
        "Heuristica 2": lambda p: aStarSearch(p, foodHeuristic),
    }

    resultados = {nombre: _medir(layout_name, nombre, f) for nombre, f in heuristicas.items()}

    print(f"{'Heuristica':14s} {'Costo':>6s} {'Longitud':>9s} {'Expandidos':>11s} {'Tiempo (s)':>12s}")
    for nombre, (costo, longitud, expandidos, tiempo) in resultados.items():
        print(f"{nombre:14s} {costo:6d} {longitud:9d} {expandidos:11d} {tiempo:12.6f}")

    costos = {c for c, _, _, _ in resultados.values()}
    assert len(costos) == 1, "las tres estrategias deberian encontrar el mismo costo optimo"

    exp0 = resultados["h(n)=0"][2]
    exp1 = resultados["Heuristica 1"][2]
    exp2 = resultados["Heuristica 2"][2]
    assert exp1 <= exp0 and exp2 <= exp0, "una heuristica admisible no deberia expandir mas que h=0"
    print(f"Heuristica 1 expande {exp0 - exp1} nodos menos que h=0 ({exp0} -> {exp1}).")
    print(f"Heuristica 2 expande {exp0 - exp2} nodos menos que h=0 ({exp0} -> {exp2}), "
          f"y {exp1 - exp2} menos que Heuristica 1 ({exp1} -> {exp2}).")
    print()


def comparar_cache(layout_name):
    print("=" * 78)
    print(f"Actividad 11 - Reto de cache (Heuristica 2 con/sin problem.heuristicInfo) en '{layout_name}'")
    print("=" * 78)

    tiempos_con, tiempos_sin = [], []
    for _ in range(REPETICIONES_CACHE):
        _, _, exp_con, t_con = _medir(
            layout_name, "H2_con_cache", lambda p: aStarSearch(p, foodHeuristic), guardar=False
        )
        _, _, exp_sin, t_sin = _medir(
            layout_name, "H2_sin_cache", lambda p: aStarSearch(p, foodHeuristicV2SinCache), guardar=False
        )
        tiempos_con.append(t_con)
        tiempos_sin.append(t_sin)

    prom_con = sum(tiempos_con) / len(tiempos_con)
    prom_sin = sum(tiempos_sin) / len(tiempos_sin)

    # Se guarda solo el promedio de cada version (misma cantidad de nodos
    # expandidos en ambas, por construccion: es la misma heuristica).
    guardar_fila({
        "actividad": "11", "metodo_heuristica": "H2_con_cache", "layout": layout_name,
        "costo": "-", "longitud_camino": "-", "nodos_expandidos": exp_con,
        "tiempo_seg": f"{prom_con:.6f}", "optimo": "si",
    })
    guardar_fila({
        "actividad": "11", "metodo_heuristica": "H2_sin_cache", "layout": layout_name,
        "costo": "-", "longitud_camino": "-", "nodos_expandidos": exp_sin,
        "tiempo_seg": f"{prom_sin:.6f}", "optimo": "si",
    })

    print(f"Nodos expandidos (identicos en ambas, misma heuristica): {exp_con}")
    print(f"Tiempo promedio CON cache ({REPETICIONES_CACHE} corridas): {prom_con:.6f}s "
          f"{[round(t,5) for t in tiempos_con]}")
    print(f"Tiempo promedio SIN cache ({REPETICIONES_CACHE} corridas): {prom_sin:.6f}s "
          f"{[round(t,5) for t in tiempos_sin]}")
    diferencia_pct = (prom_sin / prom_con - 1) * 100 if prom_con > 0 else 0
    print(f"Diferencia: {diferencia_pct:+.1f}% (sin cache vs. con cache).")
    print()


if __name__ == "__main__":
    for layout_name in LAYOUTS_COMPARACION:
        comparar_heuristicas(layout_name)

    for layout_name in LAYOUTS_CACHE:
        comparar_cache(layout_name)

    print("Filas guardadas en resultados/resultados.csv (actividad=11).")

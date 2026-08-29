"""
Actividad 8 - Heuristica para CornersProblem (dos versiones)
==================================================================
Guia: "Taller Busqueda Informada con Pac-Man", Actividad 8.

Se implementaron dos heuristicas para CornersProblem en searchAgents.py:

  Heuristica basica (cornersHeuristicBasica): la formula que sugiere la
  guia como primera aproximacion, la distancia Manhattan a la esquina
  pendiente mas lejana:
      h(n) = max_{c en C_p} d_M(n, c)

  Heuristica propuesta (cornersHeuristic, la que usa AStarCornersAgent):
  el diametro Manhattan del conjunto {posicion actual} U {esquinas
  pendientes} -- generaliza la basica considerando tambien la distancia
  entre pares de esquinas, no solo la distancia desde Pac-Man.

Este script reproduce, sobre tinyCorners, la tabla que pide la guia
(h(n)=0 / basica / propuesta) y verifica lo que la guia exige de forma
empirica para que una heuristica se considere valida:

  1. Las tres estrategias A* (h=0, basica, propuesta) encuentran el MISMO
     costo optimo (22, el mismo que dio UCS en la Actividad 7) -- si alguna
     heuristica no admisible sobreestimara, A* podria devolver un costo
     mayor al optimo, lo cual NO ocurre aqui.
  2. En el estado inicial, ninguna heuristica supera el costo optimo real
     conocido (h(inicio) <= h*(inicio) = 22): condicion necesaria de
     admisibilidad, verificada aqui puntualmente; la prueba general (para
     CUALQUIER estado, no solo el inicial) se demuestra por escrito en el
     informe usando la desigualdad triangular de la distancia Manhattan.
  3. Ninguna heuristica admisible expande MAS nodos que h(n)=0 (una
     heuristica admisible nunca hace que A* explore de mas que sin
     heuristica).

Ejecucion:
    python experimentos/actividad8_corners_heuristica.py
"""
import time

from _bootstrap import bootstrap

bootstrap()

import layout as layout_module
import pacman
from searchAgents import CornersProblem, cornersHeuristicBasica, cornersHeuristic
from search import aStarSearch, nullHeuristic

from _resultados import guardar_fila

LAYOUT_PRINCIPAL = "tinyCorners"
COSTO_OPTIMO_CONOCIDO = 22  # de la Actividad 7 (UCS sobre tinyCorners)


def _nuevo_problema(layout_name):
    lay = layout_module.getLayout(layout_name)
    state = pacman.GameState()
    state.initialize(lay, numGhostAgents=0)
    return CornersProblem(state)


def _medir(layout_name, nombre, funcion_busqueda):
    problem = _nuevo_problema(layout_name)

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded

    guardar_fila({
        "actividad": "8",
        "metodo_heuristica": nombre,
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
    })
    return costo, len(acciones), expandidos, tiempo


def verificar_admisibilidad_estado_inicial(layout_name):
    problem = _nuevo_problema(layout_name)
    inicio = problem.getStartState()

    h_basica = cornersHeuristicBasica(inicio, problem)
    h_propuesta = cornersHeuristic(inicio, problem)

    print(f"Estado inicial: {inicio}")
    print(f"  h*(inicio) real (costo optimo, Actividad 7) = {COSTO_OPTIMO_CONOCIDO}")
    print(f"  h_basica(inicio)    = {h_basica}  "
          f"({'OK, no sobreestima' if h_basica <= COSTO_OPTIMO_CONOCIDO else 'FALLA: sobreestima'})")
    print(f"  h_propuesta(inicio) = {h_propuesta}  "
          f"({'OK, no sobreestima' if h_propuesta <= COSTO_OPTIMO_CONOCIDO else 'FALLA: sobreestima'})")
    assert h_basica <= COSTO_OPTIMO_CONOCIDO, "cornersHeuristicBasica sobreestima en el estado inicial"
    assert h_propuesta <= COSTO_OPTIMO_CONOCIDO, "cornersHeuristic sobreestima en el estado inicial"
    assert h_propuesta >= h_basica, "la heuristica propuesta deberia ser al menos tan informada como la basica"
    print()


def comparar_heuristicas(layout_name):
    print("=" * 78)
    print(f"Actividad 8 - Comparacion de heuristicas de esquinas sobre '{layout_name}'")
    print("=" * 78)

    heuristicas = {
        "h(n)=0": lambda p: aStarSearch(p, nullHeuristic),
        "Heuristica basica": lambda p: aStarSearch(p, cornersHeuristicBasica),
        "Heuristica propuesta": lambda p: aStarSearch(p, cornersHeuristic),
    }

    resultados = {nombre: _medir(layout_name, nombre, f) for nombre, f in heuristicas.items()}

    print(f"{'Heuristica':22s} {'Costo':>6s} {'Longitud':>9s} {'Expandidos':>11s} {'Tiempo (s)':>12s}")
    for nombre, (costo, longitud, expandidos, tiempo) in resultados.items():
        print(f"{nombre:22s} {costo:6d} {longitud:9d} {expandidos:11d} {tiempo:12.6f}")

    costos = {c for c, _, _, _ in resultados.values()}
    assert len(costos) == 1 and COSTO_OPTIMO_CONOCIDO in costos, (
        "las tres estrategias deberian encontrar el mismo costo optimo conocido"
    )

    exp0 = resultados["h(n)=0"][2]
    expB = resultados["Heuristica basica"][2]
    expP = resultados["Heuristica propuesta"][2]
    assert expB <= exp0 and expP <= exp0, "una heuristica admisible no deberia expandir mas que h=0"
    print(f"Heuristica basica expande {exp0 - expB} nodos menos que h=0 ({exp0} -> {expB}).")
    print(f"Heuristica propuesta expande {exp0 - expP} nodos menos que h=0 ({exp0} -> {expP}), "
          f"y {expB - expP} menos que la basica ({expB} -> {expP}).")
    print()


if __name__ == "__main__":
    verificar_admisibilidad_estado_inicial(LAYOUT_PRINCIPAL)
    comparar_heuristicas(LAYOUT_PRINCIPAL)
    print("Filas guardadas en resultados/resultados.csv (actividad=8).")

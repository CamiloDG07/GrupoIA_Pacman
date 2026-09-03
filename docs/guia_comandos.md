---
title: Guía de comandos por actividad — datos y visualización
---

# Guía de comandos por actividad

Todos los comandos se corren desde una terminal de VS Code. Hay tres tipos
de comando por actividad:

- **Comando de datos**: corre el script de `experimentos/`, imprime texto
  con los números (nodos expandidos, costo, tiempo) y los guarda en
  `resultados/resultados.csv`. Se corre **desde la raíz del proyecto**
  (la carpeta `GrupoIA_Pacman`). Requiere el repositorio completo (usa
  `experimentos/_bootstrap.py` y `experimentos/_resultados.py`).
- **Comando de datos (solo con el entregable)**: `python searchAgents.py N`,
  donde `N` es el número de actividad (1 a 11). Corre **desde dentro de
  `pacman/`** y muestra exactamente los mismos números que el comando de
  datos de arriba, pero sin depender de `experimentos/` — la misma lógica
  vive ahora al final de `pacman/searchAgents.py` (funciones
  `demo_actividadN`), que es uno de los 4 archivos del zip de entrega. Por
  eso este comando es el que **sí funciona** si el profesor evalúa
  poniendo solo `search.py`, `searchAgents.py`, `resultados.csv` e
  `informe.pdf` (el contenido de `Grupo04_Pacman_AStar.zip`) sobre su
  propio proyecto base (`pacman.py`, `layout.py`, `game.py`, `util.py`,
  `layouts/`, etc.), sin la carpeta `experimentos/` ni el resto del
  repositorio. Sin argumentos (`python searchAgents.py`) corre las 11
  actividades en orden; con varios números (`python searchAgents.py 7 8 9`)
  corre solo esas.
- **Comando visual**: abre la ventana gráfica de Pacman para *ver* al
  personaje moverse siguiendo el algoritmo. Se corre **desde dentro de
  `pacman/`** (`cd pacman` primero). Es opcional — sirve para entender o
  para mostrarle al profesor, pero los números del informe siempre salen
  del comando de datos, no de mirar la ventana.

## Qué significa cada flag de `pacman.py`

| Flag | Qué es | Ejemplo |
|---|---|---|
| `-l` | Layout (mapa) a usar | `-l tinyMaze`, `-l mediumClassic` |
| `-p` | Agente (quién juega) | `-p SearchAgent` (el genérico), o uno ya armado como `-p AStarCornersAgent` |
| `-a` | Argumentos del agente: `fn` (algoritmo), `heuristic` (heurística), `prob` (tipo de problema) | `-a fn=ucs`, `-a fn=astar,heuristic=manhattanHeuristic` |
| `-q` | Sin ventana gráfica (quiet) — lo usan los scripts de `experimentos/` internamente, no hace falta que tú lo pongas a mano | `-q` |

Si no pones `prob=...`, por defecto usa `PositionSearchProblem` (el de
posición simple). Para las esquinas o la comida hay que decirlo
explícitamente: `prob=CornersProblem` o `prob=FoodSearchProblem`.

---

## Actividad 1 — Exploración del entorno

- **Datos:** `python experimentos/actividad1_exploracion.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 1`
- **Visual:** `python pacman.py -l tinyMaze` (mueves tú mismo con las flechas, no hay algoritmo todavía)

## Actividad 2 — Búsqueda de costo uniforme (UCS)

- **Datos:** `python experimentos/actividad2_ucs.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 2`
- **Visual:** `python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs`

## Actividad 3 — Implementación de A* (verificación contra UCS)

- **Datos:** `python experimentos/actividad3_astar_verificacion.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 3`
- **Visual (A* con h=0, debe verse igual que UCS):** `python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=nullHeuristic`

## Actividad 4 — A* sin información (h(n)=0) vs. UCS

- **Datos:** `python experimentos/actividad4_astar_nulo.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 4`
- **Visual UCS:** `python pacman.py -l mediumClassic -p SearchAgent -a fn=ucs`
- **Visual A*+h=0:** `python pacman.py -l mediumClassic -p SearchAgent -a fn=astar,heuristic=nullHeuristic`

## Actividad 5 — A* con distancia Manhattan

- **Datos:** `python experimentos/actividad5_manhattan.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 5`
- **Visual:** `python pacman.py -l mediumClassic -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`

## Actividad 6 — Distancia Euclidiana

- **Datos:** `python experimentos/actividad6_euclidiana.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 6`
- **Visual:** `python pacman.py -l mediumClassic -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic`

## Actividad 7 — Problema de las cuatro esquinas (diseño del estado)

- **Datos:** `python experimentos/actividad7_corners_estado.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 7`
- **Visual (UCS sobre el problema de esquinas):** `python pacman.py -l tinyCorners -p SearchAgent -a fn=ucs,prob=CornersProblem`

## Actividad 8 — Heurística para las esquinas

- **Datos:** `python experimentos/actividad8_corners_heuristica.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 8`
- **Visual (heurística básica):** `python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristicBasica`
- **Visual (heurística propuesta, la buena):** `python pacman.py -l tinyCorners -p AStarCornersAgent` (este agente ya trae la heurística propuesta configurada por defecto)

## Actividad 9 — Experimento comparativo (esquinas)

- **Datos:** `python experimentos/actividad9_corners_comparacion.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 9`
- **Visual:** igual que Actividad 8 (son los mismos 4 métodos comparados en una tabla)

## Actividad 10 — Búsqueda de todos los alimentos (FoodSearchProblem)

- **Datos:** `python experimentos/actividad10_food_baseline.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 10`
- **Visual (UCS):** `python pacman.py -l tinySearch -p SearchAgent -a fn=ucs,prob=FoodSearchProblem`
- **Visual (A*+h=0):** `python pacman.py -l tinySearch -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=nullHeuristic`

## Actividad 11 — Diseño de heurísticas para la búsqueda de alimentos

- **Datos:** `python experimentos/actividad11_food_heuristic.py`
- **Datos (solo con el entregable):** `cd pacman && python searchAgents.py 11`
- **Visual (heurística final, la que usa el proyecto):** `python pacman.py -l testClassic -p AStarFoodSearchAgent` (este agente ya trae `foodHeuristic` configurada por defecto)

⚠️ No uses `smallClassic` para probar UCS puro en Actividad 10/11 sin
límite de tiempo — tiene 55 alimentos y la explosión combinatoria hace que
UCS no termine nunca (esto ya se documentó como hallazgo en el informe).
`testClassic` (8 alimentos) es el más grande que sí es viable.

---

## ¿Correr estos comandos es lo único que hay que hacer?

No — correrlos es el paso de **verificar y generar evidencia**, no todo
el trabajo. El código (los algoritmos, las heurísticas) ya está
implementado en `pacman/search.py` y `pacman/searchAgents.py`; correr los
comandos de datos es lo que confirma que funciona y te da los números
reales. Lo que falta hacer con esos comandos, por actividad, es:

1. Correr el comando de datos y mirar la salida.
2. Contrastarla con la sección correspondiente en `docs/latex/secciones/actividadNN_*.tex`
   (el informe) y en `docs/guia_codigos_clave.md` (la explicación de qué
   hace el código y por qué) — para que entiendas *por qué* salió ese
   número, no solo que salió.
3. Opcionalmente, correr el comando visual para verlo con tus propios ojos
   y poder mostrarlo en la sustentación si el profesor lo pide.
4. Si vas a tomar los pantallazos reales de código (ver
   `docs/latex/capturas/README_capturas.md`), hacerlo también por
   actividad.

Es decir: los comandos te dan la evidencia y el entendimiento, pero el
informe y la guía de estudio (`docs/guia_codigos_clave.md`) ya están
escritos — tu trabajo ahora es *entenderlos*, no producirlos desde cero.

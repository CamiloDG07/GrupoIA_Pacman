# Sustentación — Actividad 3: Implementación de A*

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se implementó `aStarSearch` en `pacman/search.py`, reutilizando el mismo esqueleto de
`uniformCostSearch` (Actividad 2) y cambiando solo la prioridad de la cola de `g(n)` a
`f(n) = g(n) + h(n)`. Se verificó contra la línea base de UCS en 5 layouts
(`experimentos/actividad3_astar_verificacion.py`). De ahí salió un hallazgo importante: `mediumMaze`
no diferencia heurísticas (es un pasillo), así que se adoptó `mediumClassic` como layout principal
para las Actividades 4-9.

**Actualización posterior (al preparar la Actividad 11):** se encontró que `util.PriorityQueue`
(basada en `heapq`) revienta con `TypeError` al comparar estados no ordenables (el `Grid` de comida
en `FoodSearchProblem`) cuando dos entradas empatan en prioridad. Se corrigió agregando un contador
de desempate único en la tupla de la frontera, tanto en `uniformCostSearch` como en `aStarSearch`.
La corrección no cambia ningún costo óptimo, pero sí cambia el número exacto de "nodos expandidos"
reportado (el criterio de desempate afecta qué nodo empatado se expande primero). Todos los números
de este documento y del informe ya están re-verificados con la versión corregida.

## Partes críticas del código

- **`startPriority = 0 + heuristic(startState, problem)`** — el estado inicial también entra a la
  cola con prioridad `f(n)`, no con prioridad 0; si se olvida sumar la heurística aquí, el primer
  paso del algoritmo ya estaría mal.
- **La heurística se recalcula en cada sucesor, no se guarda en `bestCost`** — `bestCost` solo
  guarda `g(n)` (el costo real acumulado); `h(n)` se vuelve a calcular al generar cada sucesor con
  `heuristic(successor, problem)`. Esto es intencional: la heurística depende únicamente del
  estado, no del camino recorrido para llegar a él.
- **Es el mismo esqueleto que UCS** — esto es el punto central para la sustentación: A* no es un
  algoritmo distinto, es UCS con una función de prioridad distinta. Cualquier pregunta sobre
  "diferencias entre UCS y A*" se responde señalando esta única línea de diferencia.

## ¿Qué pasa si...?

- **¿Qué pasa si la heurística no es admisible (sobreestima el costo real)?**
  A* podría dejar de ser óptimo: podría reportar como solución un camino más costoso que el
  óptimo, porque una heurística que sobreestima puede hacer que un nodo en el camino óptimo
  parezca (falsamente) más caro que una alternativa peor, y ese nodo nunca llegue a expandirse a
  tiempo. Esto se analiza formalmente en la sección "Admisibilidad" de la guía (Actividad 8).
- **¿Qué pasa si se quita el chequeo `if cost > bestCost.get(state, ...): continue`?**
  El algoritmo seguiría terminando y encontrando el costo óptimo (porque solo se insertan sucesores
  con costo estrictamente mejor), pero podría reprocesar entradas obsoletas de la cola,
  desperdiciando trabajo sin cambiar el resultado.
- **¿Qué pasa si a `aStarSearch` se le pasa `heuristic=uniformCostSearch`'s falta de heurística,
  es decir, no se pasa ningún argumento?**
  Usa el valor por defecto `nullHeuristic` (que siempre devuelve 0), y A* se comporta exactamente
  igual que UCS — esto es justo lo que se demuestra y explica en la Actividad 4.

## Preguntas trampa esperadas del profesor

1. **"¿Por qué A* con h=0 expandió exactamente el mismo número de nodos que UCS, ni uno más ni
   uno menos, en los 5 layouts probados?"**
   Porque con `h(n) = 0`, la fórmula `f(n) = g(n) + h(n)` se reduce a `f(n) = g(n)`: es la misma
   prioridad que usa UCS, así que ambos algoritmos exploran la frontera exactamente en el mismo
   orden. No es una coincidencia experimental, es una consecuencia directa de la fórmula.
2. **"¿Por qué en `mediumMaze` ninguna heurística ayudó, pero en `mediumClassic` sí?"**
   Porque `mediumMaze` es un pasillo sin bifurcaciones entre el inicio y la meta: solo existe una
   secuencia de movimientos posible en cada punto, así que no hay ninguna decisión donde una
   heurística pueda "orientar" la búsqueda. `mediumClassic` sí tiene bifurcaciones reales, y ahí
   Manhattan reduce los nodos expandidos de 69 a 15.
3. **"Si cambio el orden en que se generan los sucesores dentro de `getSuccessors` (por ejemplo,
   probando primero West en vez de North), ¿cambia el resultado de A*?"**
   El costo óptimo encontrado no cambia (A* sigue siendo óptimo con una heurística admisible), pero
   el número exacto de nodos expandidos sí puede cambiar ligeramente cuando hay empates de
   prioridad, porque `util.PriorityQueue` no rompe empates por orden de inserción de forma
   determinista más allá del heap subyacente.

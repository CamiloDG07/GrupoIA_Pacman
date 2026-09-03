# Sustentación — Actividad 2: Búsqueda de costo uniforme (UCS)

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se implementó `uniformCostSearch` en `pacman/search.py`: búsqueda en grafo con
`util.PriorityQueue` ordenada por `g(n)`, con un diccionario `bestCost` para no re-expandir
un estado cuando ya se conoce un camino más barato hacia él. Medido con `demo_actividad2()`
(`pacman/searchAgents.py`, `python searchAgents.py 2`) sobre `mediumMaze` (línea base: costo 30,
32 nodos expandidos).

## Partes críticas del código

- **La cola de prioridad usa `g(n)` puro, sin heurística** — es la única diferencia estructural
  con A* (Actividad 3): mismo esqueleto de algoritmo, cambia solo la prioridad usada al insertar
  en `frontier`.
- **`if cost > bestCost.get(state, float('inf')): continue`** — esta línea es la que hace que el
  algoritmo sea correcto y eficiente a la vez sin necesitar `decrease-key`: en vez de actualizar
  la prioridad de un elemento ya insertado (que `util.PriorityQueue` no soporta), simplemente se
  ignoran las copias obsoletas cuando salen de la cola.
- **La prueba de meta se hace al extraer el nodo de la frontera, no al generarlo como sucesor**
  (patrón "goal test on pop"): esto es lo que garantiza optimalidad en UCS, porque el primer nodo
  meta que se extrae con la prioridad más baja es, por construcción, el de menor costo.

## ¿Qué pasa si...?

- **¿Qué pasa si quito el chequeo `if cost > bestCost.get(...): continue`?**
  El algoritmo seguiría terminando (porque `newCost < bestCost.get(...)` en el fondo evita
  reinsertar caminos peores), pero podría expandir nodos redundantes con costos ya superados,
  gastando más tiempo sin cambiar el resultado final (la solución sigue siendo óptima, solo menos
  eficiente).
- **¿Qué pasa si pruebo el objetivo al generar el sucesor en vez de al extraerlo de la cola
  (`isGoalState` dentro de `getSuccessors`)?**
  Se perdería la garantía de optimalidad de UCS: se podría reportar como solución el primer camino
  que *llegue* a la meta, no el más barato, porque un camino más corto en pasos pero más costoso
  podría generarse antes de que se procese el más barato.
- **¿Qué pasa si corro `python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs` directamente
  (sin `-q` y sin pasar por `demo_actividad2()`)?**
  Se ve exactamente el mismo costo/nodos/tiempo impresos, pero el proceso termina con
  `Exception: Illegal action Stop` justo después. Es un efecto secundario de que estos layouts
  traen mucha comida extra (no solo un pellet en la meta) y `SearchAgent` (que no se debe tocar)
  devuelve `Stop` cuando se le acaban las acciones del plan; en este motor `Stop` nunca es una
  acción legal. No afecta el resultado de la búsqueda: la medición ya ocurrió antes del error.

## Preguntas trampa esperadas del profesor

1. **"¿UCS es lo mismo que Dijkstra?"**
   Sí, conceptualmente: ambos expanden siempre el nodo de menor costo acumulado conocido con una
   cola de prioridad. UCS es la versión de Dijkstra formulada como búsqueda en un problema con
   estado inicial y prueba de meta (no necesariamente calcula distancias a *todos* los nodos, se
   detiene apenas encuentra la meta).
2. **"¿Por qué la longitud del camino es igual al costo en esta actividad?"**
   Porque el costo por paso es 1 para todas las acciones en `PositionSearchProblem` (su `costFn`
   por defecto es `lambda x: 1`); en problemas con costos distintos por acción (como
   `StayEastSearchAgent`/`StayWestSearchAgent`, ya presentes en `searchAgents.py`), costo y
   longitud dejarían de coincidir.
3. **"¿Qué garantiza que UCS sea óptimo? ¿Y completo?"**
   Es completo si el espacio de estados es finito (o si existe solución con costo finito) porque
   explora en orden no decreciente de costo; es óptimo por esa misma razón: no puede reportar una
   meta con costo mayor mientras exista en la frontera un camino con costo menor sin explorar.

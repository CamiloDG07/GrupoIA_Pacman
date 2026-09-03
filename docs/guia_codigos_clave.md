---
title: Guía de código clave por actividad — para pantallazos y para estudiar
---

# Guía de código clave por actividad

Este documento tiene dos usos:

1. **Para el informe**: te dice exactamente qué pantallazo tomar en VS Code
   para cada actividad (archivo + líneas + función), para reemplazar los
   bloques de código escritos como texto por capturas reales (ver
   `docs/latex/capturas/README_capturas.md` para el paso a paso de cómo
   reemplazar cada imagen).
2. **Para estudiar / sustentación**: cada sección explica **qué hace** el
   código, **cómo funciona** paso a paso, **por qué se hizo así** (qué se
   modificó y por qué era necesario para esa actividad), y **cómo afecta**
   a los resultados medidos — con los números reales del proyecto, no
   genéricos.

Todos los números citados aquí salen de `resultados/resultados.csv` y ya
están verificados y usados en `informe.pdf`.

---

## Actividad 1. Exploración del entorno

**📸 Qué capturar (opcional, no hay código nuevo):** `pacman/searchAgents.py`,
líneas 120-194, clase `PositionSearchProblem` (ya viene dada por el
profesor; no se modifica). Si quieres un pantallazo para esta actividad,
esta es la clase que se está "explorando".

```python
class PositionSearchProblem(search.SearchProblem):
    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True):
        ...

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        return state == self.goal

    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH,
                       Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))
        return successors
```

**Qué hace:** define el problema de búsqueda más simple posible: el estado
es solo una posición `(x, y)`, hay 4 acciones posibles (las direcciones
cardinales), un sucesor es válido si la celda vecina no es pared, y la meta
es una única posición fija (`self.goal`). El goal y el costo de cada paso
no se calculan a mano: son los parámetros `goal` y `costFn` de
`__init__` (línea 131), con valor por defecto `goal=(1,1)` y
`costFn = lambda x: 1` (esa lambda ignora el estado que recibe y siempre
devuelve 1) si no se especifica lo contrario al construir el problema.

**Cómo funciona:** por cada dirección, calcula la celda vecina sumando el
vector de esa dirección a la posición actual; si esa celda no tiene pared,
la agrega como sucesor con costo `self.costFn(nextState)` (1 por defecto).

**Por qué es la parte clave:** no se modificó nada aquí (el profesor ya la
entrega completa), pero es la pieza que hay que entender **antes** de
implementar UCS/A* en las Actividades 2-3: es el contrato exacto que espera
`getSuccessors` (retornar tripletas `(sucesor, acción, costo)`) y que se
reutiliza sin cambios en `CornersProblem` (Actividad 7) y
`FoodSearchProblem` (Actividad 10), solo que en esos problemas el **estado**
deja de ser solo `(x,y)`.

**Cómo afecta a los resultados:** ninguno directamente (no se mide nada en
esta actividad), pero es la base conceptual: todo el resto del laboratorio
consiste en generalizar este mismo patrón (estado, sucesores, meta, costo)
a problemas donde el estado necesita más información.

---

## Actividad 2. Búsqueda de costo uniforme (UCS)

**📸 Qué capturar:** `pacman/search.py`, líneas 80-120, función
`uniformCostSearch`.

```python
def uniformCostSearch(problem):
  frontier = util.PriorityQueue()
  startState = problem.getStartState()
  contador = 0
  frontier.push((contador, startState, [], 0), 0)
  bestCost = {startState: 0}

  while not frontier.isEmpty():
    _, state, actions, cost = frontier.pop()
    if cost > bestCost.get(state, float('inf')):
      continue
    if problem.isGoalState(state):
      return actions
    for successor, action, stepCost in problem.getSuccessors(state):
      newCost = cost + stepCost
      if newCost < bestCost.get(successor, float('inf')):
        bestCost[successor] = newCost
        contador += 1
        frontier.push((contador, successor, actions + [action], newCost), newCost)
  return []
```

**Qué hace:** implementa búsqueda en grafo con una cola de prioridad
ordenada por `g(n)` (el costo acumulado real desde el inicio). Extrae
siempre el estado con menor costo conocido, prueba si es meta, y si no lo
es, expande sus sucesores.

**Cómo funciona, paso a paso:**
1. Se inserta el estado inicial en la frontera con costo 0.
2. En cada iteración se extrae (`pop`) el elemento de menor prioridad.
3. Si ese costo es peor que el mejor ya conocido para ese estado
   (`bestCost`), es una entrada obsoleta de la cola → se descarta sin
   expandir (`continue`). Esto pasa porque `util.PriorityQueue` no soporta
   *decrease-key*: en vez de actualizar una entrada ya insertada, se
   vuelve a insertar el estado con su nuevo costo, y las copias viejas se
   filtran aquí.
4. Se prueba la meta **antes** de expandir (evita expandir de más).
5. Por cada sucesor, si el nuevo costo mejora lo que ya se conocía de él,
   se actualiza `bestCost` y se agrega a la frontera.

**Por qué es la parte clave / qué se modificó:** este es el algoritmo
completo que había que implementar desde cero (el archivo original solo
trae la función vacía). El detalle más importante para defender es el
**contador de desempate** (`contador`): cada elemento de la frontera es una
tupla `(contador, estado, acciones, costo)`, no `(estado, acciones, costo)`.
La razón: `util.PriorityQueue` usa `heapq`, que compara tuplas completas
cuando hay empate de prioridad; si el estado no es comparable (como el
`Grid` de comida en `FoodSearchProblem`, Actividades 10-11), Python lanza
`TypeError: '<' not supported between instances of 'Grid' and 'Grid'`. Como
el contador es único y creciente, `heapq` nunca necesita mirar más allá de
él para romper el empate.

**Cómo afecta a los resultados:** UCS es la línea base de todo el informe.
Sobre `mediumClassic` expande **69 nodos** con costo óptimo 12 — ese 69 es
el número contra el que se comparan *todas* las heurísticas de las
Actividades 4-6. Sin el contador de desempate, el algoritmo directamente
falla (no da ningún número) apenas se corre sobre `FoodSearchProblem`.

---

## Actividad 3. Implementación de A*

**📸 Qué capturar:** `pacman/search.py`, líneas 129-172, función
`aStarSearch`.

```python
def aStarSearch(problem, heuristic=nullHeuristic):
  frontier = util.PriorityQueue()
  startState = problem.getStartState()
  contador = 0
  startPriority = 0 + heuristic(startState, problem)  # f = g + h
  frontier.push((contador, startState, [], 0), startPriority)
  bestCost = {startState: 0}

  while not frontier.isEmpty():
    _, state, actions, cost = frontier.pop()
    if cost > bestCost.get(state, float('inf')):
      continue
    if problem.isGoalState(state):
      return actions
    for successor, action, stepCost in problem.getSuccessors(state):
      newCost = cost + stepCost
      if newCost < bestCost.get(successor, float('inf')):
        bestCost[successor] = newCost
        contador += 1
        priority = newCost + heuristic(successor, problem)  # f(n) = g(n) + h(n)
        frontier.push((contador, successor, actions + [action], newCost), priority)
  return []
```

**Qué hace:** es *exactamente* el mismo esqueleto que `uniformCostSearch`
(misma frontera, mismo `bestCost`, mismo goal-test antes de expandir). La
**única línea que cambia de verdad** es la prioridad: en vez de `newCost`
(que es `g(n)`), se usa `priority = newCost + heuristic(successor, problem)`
(que es `f(n) = g(n) + h(n)`).

**Cómo funciona:** al insertar cualquier estado en la frontera, su
prioridad ya no es solo "qué tan caro fue llegar hasta aquí" (`g(n)`) sino
"qué tan caro fue llegar más lo que falta estimar" (`g(n) + h(n)`). Eso hace
que la cola priorice estados que combinan bajo costo acumulado **y**
parecen estar cerca de la meta según la heurística.

**Por qué es la parte clave / qué se modificó:** se implementó A* como
generalización de UCS, reutilizando el mismo contador de desempate por el
mismo motivo (evitar `TypeError` con estados no comparables). Es importante
poder señalar, comparando esta función con la de UCS, que **la diferencia
real entre los dos algoritmos es una sola línea** — esto es justamente la
Pregunta de análisis de la Actividad 4.

**Cómo afecta a los resultados:** con `heuristic=nullHeuristic` (h=0), A*
da exactamente los mismos números que UCS en los 5 layouts probados (por
ejemplo 69 nodos en `mediumClassic`, 295 en `tinyCorners`) — es la
verificación de que la implementación es correcta antes de meterle
heurísticas no triviales. Con Manhattan, en `mediumClassic` pasa de 69 a
**15** nodos expandidos.

---

## Actividad 4. A* sin información ($h(n)=0$)

No hay código nuevo aquí (se reutiliza `aStarSearch` de la Actividad 3 con
`nullHeuristic`, ya provista):

```python
def nullHeuristic(state, problem=None):
  return 0
```

**Qué hace:** una heurística "constante cero" — nunca aporta información.

**Por qué es la parte clave:** demuestra algebraicamente que **UCS es un
caso particular de A***. Si `h(n) = 0` para todo `n`, entonces
`f(n) = g(n) + 0 = g(n)`, que es exactamente la prioridad de UCS. Como
ambos usan la misma cola de prioridad con la misma prioridad, expanden los
mismos nodos en el mismo orden.

**Cómo afecta a los resultados:** en `mediumClassic`, UCS y A*+h=0 dan
**ambos costo 12 y 69 nodos expandidos** — coinciden exactamente. Lo mismo
se repite en `tinyCorners` (295 nodos) y en `testClassic` con comida (2598
nodos). Esta coincidencia exacta, repetida en tres problemas distintos, es
la evidencia de que no es casualidad sino una consecuencia directa de la
fórmula de `f(n)`.

---

## Actividad 5. A* con distancia Manhattan

**📸 Qué capturar:** `pacman/searchAgents.py`, líneas 236-240, función
`manhattanHeuristic`.

```python
def manhattanHeuristic(position, problem, info={}):
  xy1 = position
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
```

**Qué hace:** calcula $h_M(n) = |x_n-x_g| + |y_n-y_g|$: la suma de
diferencias absolutas en cada eje.

**Cómo funciona:** es el número mínimo de movimientos ortogonales
(norte/sur/este/oeste) que se necesitarían para llegar de `n` a la meta
**si no hubiera paredes**. Como Pac-Man solo se mueve en 4 direcciones
cardinales, esta métrica coincide exactamente con la noción de "cercanía"
de este espacio de acciones.

**Por qué es la parte clave:** esta función ya viene dada por el profesor
(no hubo que escribirla), pero es la primera heurística *no trivial* que se
usa: al ignorar las paredes nunca sobreestima el costo real, por lo que es
admisible por construcción.

**Cómo afecta a los resultados:** en `mediumClassic`, A*+Manhattan expande
**15 nodos** contra los 69 de UCS — 4.6 veces menos, sin cambiar el costo
óptimo (12). Es la primera vez en el informe que se ve una reducción real
de exploración gracias a una heurística.

---

## Actividad 6. A* con distancia Euclidiana

**📸 Qué capturar:** `pacman/searchAgents.py`, líneas 242-246, función
`euclideanHeuristic`.

```python
def euclideanHeuristic(position, problem, info={}):
  xy1 = position
  xy2 = problem.goal
  return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5
```

**Qué hace:** calcula $h_E(n) = \sqrt{(x_n-x_g)^2+(y_n-y_g)^2}$: la
distancia en línea recta entre `n` y la meta.

**Por qué es la parte clave:** sirve para comparar contra Manhattan y
responder la pregunta de análisis de la guía (¿cuál heurística representa
mejor el movimiento de Pac-Man?). Matemáticamente $h_E(n) \le h_M(n)$
siempre (la hipotenusa nunca es más larga que la suma de catetos), así que
Euclidiana es una cota **menos ajustada** — más conservadora, menos
informativa.

**Cómo afecta a los resultados:** en `mediumClassic`, Euclidiana expande
**16 nodos** contra los 15 de Manhattan (misma tendencia, más marcada en
`openClassic`: 31 vs. 27). Esta pequeña diferencia consistente es la
evidencia experimental de que Manhattan, al ser una cota más ajustada, guía
mejor la búsqueda sin dejar de ser admisible.

---

## Actividad 7. Problema de las cuatro esquinas — diseño del estado

**📸 Qué capturar (2 pantallazos):** `pacman/searchAgents.py`, `getStartState`,
`isGoalState` y `getSuccessors` de `CornersProblem` no entran completas en una
sola pantalla, así que van en 2 capturas: líneas 273-309 (parte 1: `getStartState`,
`isGoalState` y el inicio de `getSuccessors`) y líneas 309-336 (parte 2: resto
de `getSuccessors`, la construcción del sucesor).

```python
def getStartState(self):
    esquinasVisitadas = (False, False, False, False)
    return (self.startingPosition, esquinasVisitadas)

def isGoalState(self, state):
    _, esquinasVisitadas = state
    return all(esquinasVisitadas)

def getSuccessors(self, state):
    successors = []
    position, visited = state
    for action in [Directions.NORTH, Directions.SOUTH,
                   Directions.EAST, Directions.WEST]:
        x, y = position
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        if not self.walls[nextx][nexty]:
            nextPosition = (nextx, nexty)
            nextVisited = visited
            if nextPosition in self.corners:
                idx = self.corners.index(nextPosition)
                if not visited[idx]:
                    nextVisited = visited[:idx] + (True,) + visited[idx+1:]
            successors.append(((nextPosition, nextVisited), action, 1))
    self._expanded += 1
    return successors
```

**Qué hace:** define el estado como el par
`(posición, esquinas_visitadas)`, donde `esquinas_visitadas` es una tupla
de 4 booleanos. La meta se alcanza cuando las 4 son `True`,
**sin importar** en qué posición esté Pac-Man.

**Cómo funciona:** al generar un sucesor, si la nueva posición coincide con
una esquina que aún no estaba marcada, se construye una tupla *nueva* con
esa esquina en `True` (las tuplas son inmutables — no se modifica la
original).

**Por qué es la parte clave / qué se modificó:** esta es la decisión de
diseño central de la actividad, y la que suele preguntarse en sustentación.
La posición sola **no alcanza** como estado: dos situaciones con la misma
posición pero distinto progreso (unas esquinas visitadas y otras no) no son
equivalentes — necesitan caminos distintos para llegar a la meta. Si el
estado fuera solo `(x,y)`, un algoritmo de búsqueda podría marcar como "ya
explorado" un estado que en realidad todavía necesita explorarse con otra
combinación de esquinas pendientes, perdiendo la garantía de optimalidad. Se
usó una tupla (no una lista) porque tiene que ser hasheable/comparable para
funcionar dentro de `util.PriorityQueue` y de los diccionarios de costo.

**Cómo afecta a los resultados:** con este estado, UCS sobre `tinyCorners`
encuentra el camino óptimo (costo 22) expandiendo **295 nodos** — ese 295
es la línea base contra la que se miden las heurísticas de las Actividades
8-9.

---

## Actividad 8. Heurísticas para CornersProblem

**📸 Qué capturar (2 pantallazos):**
- `pacman/searchAgents.py`, líneas 351-364, `cornersHeuristicBasica`.
- `pacman/searchAgents.py`, líneas 365-389, `cornersHeuristic` (la
  propuesta, usada por `AStarCornersAgent`).

```python
def cornersHeuristicBasica(state, problem):
  position, visited = state
  corners = problem.corners
  pendientes = [c for c, v in zip(corners, visited) if not v]
  if not pendientes:
    return 0
  return max(abs(position[0]-c[0]) + abs(position[1]-c[1]) for c in pendientes)


def cornersHeuristic(state, problem):
  position, visited = state
  corners = problem.corners
  pendientes = [c for c, v in zip(corners, visited) if not v]
  if not pendientes:
    return 0
  puntos = [position] + pendientes
  maxDist = 0
  for i in range(len(puntos)):
    for j in range(i + 1, len(puntos)):
      d = abs(puntos[i][0]-puntos[j][0]) + abs(puntos[i][1]-puntos[j][1])
      if d > maxDist:
        maxDist = d
  return maxDist
```

**Qué hace cada una:**
- **Básica**: $h(n) = \max_{c \in C_p} d_M(n,c)$ — la distancia Manhattan
  desde Pac-Man hasta la esquina pendiente más lejana.
- **Propuesta**: $h(n) = \max\big(\max_c d_M(n,c),\ \max_{c_i,c_j} d_M(c_i,c_j)\big)$
  — el **diámetro** Manhattan del conjunto {posición actual} ∪ {esquinas
  pendientes}: la mayor distancia entre *cualquier par* de esos puntos, no
  solo entre Pac-Man y la esquina más lejana.

**Cómo funciona la propuesta (paso a paso):** arma la lista `puntos` con la
posición actual más todas las esquinas pendientes, y recorre **todos los
pares** de esa lista calculando su distancia Manhattan, quedándose con la
máxima. Por eso es más cara de calcular que la básica (que solo mira
posición→esquina), pero con máximo 4 esquinas (6 pares) el costo extra es
insignificante.

**Por qué es la parte clave / qué se modificó:** la básica es la primera
aproximación que sugiere la guía; la propuesta la generaliza con el mismo
patrón de "diámetro" que se reutiliza en la Actividad 11 para comida. Es
más informativa porque considera que, para visitar dos esquinas lejanas
entre sí, Pac-Man tiene que recorrer *al menos* la distancia real entre
ellas en algún momento — no solo la distancia desde donde está ahora hasta
la más lejana. Ambas son admisibles y consistentes (demostrado formalmente
en `informe.pdf`, sección de Actividad 8): la Manhattan nunca sobreestima
una distancia real en una cuadrícula con paredes.

**Cómo afecta a los resultados** (sobre `tinyCorners`, costo óptimo 22 en
los tres casos):

| Heurística | Nodos expandidos | Reducción vs. h=0 |
|---|---|---|
| h(n)=0 | 295 | — |
| Básica | 147 | 49.8% |
| Propuesta | 119 | 59.7% |

La propuesta reduce un 19% adicional frente a la básica — es la evidencia
directa de que el término extra (distancia entre pares de esquinas) sí
aporta información útil, no es solo más cálculo por gusto.

---

## Actividad 9. Experimento comparativo (esquinas)

No hay código nuevo (se reutiliza todo lo de la Actividad 8; la función
`demo_actividad9()` al final de `pacman/searchAgents.py` corre las 4 estrategias
por separado y calcula el factor de reducción).

**Qué hace el experimento:** corre UCS, A*+h=0, A*+básica y A*+propuesta
sobre `tinyCorners`, cada una con su propia instancia de `CornersProblem`
(para que el contador `_expanded` de una no se mezcle con las demás), y
verifica que las 4 lleguen al mismo costo óptimo antes de reportar.

**Por qué es la parte clave:** aquí se calcula el **factor de reducción de
expansiones**:

$$R = \frac{N_{UCS}}{N_{A^*}} = \frac{295}{119} = 2.48 \quad \text{(con la propuesta)}$$

$$R = \frac{295}{147} = 2.01 \quad \text{(con la básica)}$$

**Cómo afecta a los resultados:** es la métrica que resume, en un solo
número, cuánto ayuda cada heurística: UCS tuvo que explorar 2.48 veces más
estados que A*+propuesta para llegar exactamente al mismo resultado óptimo.

---

## Actividad 10. Búsqueda de todos los alimentos (FoodSearchProblem)

**📸 Qué capturar:** `pacman/searchAgents.py`, líneas 396-417 (estado e
`isGoalState`; el archivo ya viene completo, no se modificó código aquí).

```python
class FoodSearchProblem:
  def __init__(self, startingGameState):
    self.start = (startingGameState.getPacmanPosition(),
                  startingGameState.getFood())
    ...

  def isGoalState(self, state):
    return state[1].count() == 0
```

**Qué hace:** el estado ahora es el par `(posición, foodGrid)`, donde
`foodGrid` es una matriz booleana (`Grid`) con qué alimentos siguen
presentes. La meta se alcanza cuando `foodGrid.count() == 0` (no queda
ningún alimento), sin importar dónde esté Pac-Man.

**Por qué es la parte clave:** explica por qué el espacio de estados
explota: si el laberinto tiene $F$ alimentos, cada uno puede estar
presente o consumido, así que hay $2^F$ configuraciones posibles de comida
— multiplicado por cada posición posible de Pac-Man. Es también el motivo
por el que el `Grid` como parte del estado rompe la comparación de
`heapq` si no se usa el contador de desempate de la Actividad 3 (un `Grid`
no es comparable con `<`).

**Cómo afecta a los resultados:** con solo 1 alimento (`tinySearch`), UCS
expande 16 nodos; con 8 alimentos (`testClassic`), salta a **2598 nodos**.
Se intentó `smallClassic` (55 alimentos) y **no terminó en 45 segundos**:
$2^{55}$ es astronómicamente más grande que cualquier espacio manejado
antes en el laboratorio. Este salto es la motivación directa de por qué
hace falta diseñar una heurística no trivial en la Actividad 11.

---

## Actividad 11. Heurísticas para FoodSearchProblem

**📸 Qué capturar (3 pantallazos):**
- `pacman/searchAgents.py`, líneas 452-464, `foodHeuristicV1`.
- `foodHeuristic` (con caché; la que usa `AStarFoodSearchAgent`) no entra
  completa en una sola pantalla, así que va en 2 capturas: líneas 465-488
  (parte 1, construcción del caché) y líneas 490-502 (parte 2, uso del
  caché y cálculo final de `maxDist`).

```python
def foodHeuristicV1(state, problem):
  position, foodGrid = state
  foodList = foodGrid.asList()
  if not foodList:
    return 0
  return max(abs(position[0]-f[0]) + abs(position[1]-f[1]) for f in foodList)


def foodHeuristic(state, problem):
  position, foodGrid = state
  foodList = foodGrid.asList()
  if not foodList:
    return 0

  if 'foodPairDistances' not in problem.heuristicInfo:
    allFood = problem.start[1].asList()
    distancias = {}
    for i in range(len(allFood)):
      for j in range(i + 1, len(allFood)):
        f1, f2 = allFood[i], allFood[j]
        d = abs(f1[0]-f2[0]) + abs(f1[1]-f2[1])
        distancias[(f1, f2)] = d
        distancias[(f2, f1)] = d
    problem.heuristicInfo['foodPairDistances'] = distancias

  distanciasComida = problem.heuristicInfo['foodPairDistances']
  maxDist = 0
  for f in foodList:
    d = abs(position[0]-f[0]) + abs(position[1]-f[1])
    if d > maxDist: maxDist = d
  for i in range(len(foodList)):
    for j in range(i+1, len(foodList)):
      d = distanciasComida[(foodList[i], foodList[j])]
      if d > maxDist: maxDist = d
  return maxDist
```

**Qué hace cada una:**
- **Heurística 1**: $h(n) = \max_{f \in F} d_M(n,f)$ — distancia al
  alimento restante más lejano.
- **Heurística 2**: $h(n) = \max\big(\max_f d_M(n,f),\ \max_{f_i,f_j} d_M(f_i,f_j)\big)$
  — el mismo patrón de diámetro que en `cornersHeuristic` (Actividad 8),
  ahora sobre {posición} ∪ {comida restante}.

**Cómo funciona el caché (`problem.heuristicInfo`):** las distancias entre
pares de alimentos se calculan **una sola vez** (usando
`problem.start[1]`, la comida del estado inicial) y se guardan en
`problem.heuristicInfo['foodPairDistances']`; las llamadas siguientes a la
heurística reutilizan ese diccionario en vez de recalcular la resta cada
vez. La idea es evitar repetir, miles de veces, un cálculo que no cambia
(las posiciones de la comida no se mueven, solo dejan de estar presentes).

**Por qué es la parte clave / qué se modificó:** la Heurística 2 es más
informativa que la 1 porque considera que, para visitar dos alimentos
lejanos entre sí, Pac-Man tiene que recorrer *al menos* la distancia real
entre ellos en algún momento — no solo la distancia desde su posición
actual. El caché es la optimización que sugiere la guía para el cálculo que
más se repite (distancia entre pares de alimentos).

**Hallazgo honesto sobre el caché:** medir el tiempo real con y sin caché
dio un resultado contraintuitivo: la versión **sin** caché fue ligeramente
**más rápida** (entre 4% y 7%) en los dos layouts probados. La explicación
no es que el caché esté mal — los nodos expandidos son idénticos en ambas
versiones — sino que el cálculo cacheado (una resta de enteros) es más
barato que construir una tupla `(f1,f2)` y consultar un diccionario por
ella. Es una buena respuesta si preguntan "¿por qué no mejoró el caché?" en
la sustentación: no toda optimización estándar ayuda en todo contexto, hay
que medir.

**Cómo afecta a los resultados** (sobre `testClassic`, 8 alimentos, costo
óptimo 16 en los tres casos):

| Heurística | Nodos expandidos | Factor R vs. h=0 |
|---|---|---|
| h(n)=0 | 2598 | — |
| Heurística 1 | 702 | 3.70 |
| Heurística 2 | 383 | 6.78 |

La Heurística 2 expande 319 nodos menos que la Heurística 1 — la misma
relación "más información ⟹ menos exploración" que se vio en el problema de
esquinas (Actividad 8-9), ahora confirmada en un segundo problema distinto.

---

## Resumen: la relación que atraviesa todo el laboratorio

En los tres problemas trabajados (búsqueda simple, esquinas, comida) se
repite el mismo patrón: **entre más informada es la heurística (sin dejar
de ser admisible), menos nodos expande A* para encontrar la misma solución
óptima.**

| Problema | h=0 | Heurística intermedia | Heurística final | Factor R |
|---|---|---|---|---|
| Esquinas (`tinyCorners`) | 295 | 147 (básica) | 119 (propuesta) | 2.48 |
| Comida (`testClassic`) | 2598 | 702 (H1) | 383 (H2) | 6.78 |

Si te preguntan en la sustentación "¿por qué diseñaron dos heurísticas y no
se quedaron con la primera?", esta tabla es la respuesta directa: la más
informada (la que considera el diámetro entre todos los puntos pendientes,
no solo la distancia a el más lejano) fue, en los dos problemas, la que
menos nodos expandió — sin perder nunca la optimalidad (el costo final es
idéntico en todas las filas de cada problema).

# Revisión del `search.py` que mandó el compañero (Parte 1)

## Resumen: no estaba listo para entrar tal cual. Se corrigieron 2 problemas reales, verificados
ejecutando el código (no solo leyéndolo).

## Problema 1 (grave): `uniformCostSearch` (Actividad 2) no está implementada

El archivo trae:
```python
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  util.raiseNotDefined()
```

`util.raiseNotDefined()` en este proyecto hace `sys.exit(1)` — es decir, **termina todo el proceso
de Python**, no lanza una excepción capturable. Se comprobó ejecutándola directamente: el proceso
muere con "Method not implemented: uniformCostSearch" y código de salida 1.

Esto significa que la Actividad 2 (que es justamente parte de la Parte 1, la responsabilidad del
compañero que mandó este archivo) está completamente ausente. Cualquier experimento, o el propio
profesor corriendo `-a fn=ucs`, haría fallar el proceso entero.

**Se corrigió** implementándola con el mismo patrón que ya traía `aStarSearch` en el archivo
(diccionario `explored` con re-apertura de nodos si se encuentra un costo mejor), para que el
archivo quede en un único estilo consistente.

## Problema 2 (real pero más sutil): a `aStarSearch` le falta el desempate de la cola de prioridad

El algoritmo de `aStarSearch` en sí **es correcto**: cola de prioridad con $f(n) = g(n) + h(n)$,
prueba de meta al extraer el nodo, y un diccionario `explored` que permite reabrir un estado si
aparece un camino más barato después. Es un patrón válido (aunque distinto al que usamos nosotros
en nuestra propia Actividad 3, que poda antes de insertar en vez de reabrir después).

El problema es que empuja tuplas `(estado, acciones, costo)` a la cola sin ningún contador de
desempate. `util.PriorityQueue` (ver `util.py`) usa `heapq` internamente y **no agrega ningún
tiebreaker propio** — simplemente hace `heapq.heappush(heap, (prioridad, item))`. Cuando dos
entradas empatan en prioridad, `heapq` necesita comparar `item` para decidir el orden, y ese
`item` es la tupla `(estado, acciones, costo)`.

Mientras el estado sea `(x, y)` (como en `PositionSearchProblem`), esto nunca falla: son enteros,
siempre comparables. Pero en `FoodSearchProblem` (las Actividades 10 y 11 de este taller,
exactamente la parte que le tocó a Wiston) el estado es `(posición, foodGrid)`, y `foodGrid` es un
`Grid` que no define `__lt__`. Se comprobó ejecutándolo:

```
Traceback (most recent call last):
  ...
  File ".../search.py", line 108, in aStarSearch
    current_state, actions, current_g = frontier.pop()
  File ".../util.py", line 66, in pop
    (priority,item) = heapq.heappop(self.heap)
TypeError: '<' not supported between instances of 'Grid' and 'Grid'
```

Esto pasó corriendo `aStarSearch(problem, nullHeuristic)` sobre `testClassic` con
`FoodSearchProblem` — es decir, el archivo tal como llegó **rompe exactamente la parte del trabajo
que le corresponde a Wiston**, aunque a la Parte 1 (Actividades 1-6, todas sobre
`PositionSearchProblem`) nunca le hubiera hecho falta notarlo.

**Se corrigió** agregando un contador entero único y creciente como primer elemento de cada tupla
de la frontera (`(contador, estado, acciones, costo)`); como los contadores nunca se repiten,
`heapq` nunca necesita comparar el resto de la tupla. Es exactamente el mismo fix que ya habíamos
aplicado a nuestra propia implementación (ver el commit "Corrección: tie-breaker en UCS/A*" del
repositorio) — este bug era genuinamente independiente de cómo cada quien escribió su algoritmo;
depende solo de no ponerle un desempate a la cola de prioridad cuando el estado puede no ser
comparable.

## Verificación después de corregir

Se corrió la versión corregida contra los mismos layouts de referencia que usa todo el informe:

| Prueba | Resultado |
|---|---|
| UCS en `tinyMaze` | costo=10, expandidos=21 ✓ |
| UCS en `mediumMaze` | costo=30, expandidos=32 ✓ |
| UCS en `mediumClassic` | costo=12, expandidos=69 ✓ |
| A*+Manhattan en `mediumClassic` | costo=12, expandidos=15 ✓ |
| A*+h=0 en `FoodSearchProblem`/`tinySearch` | costo=8, expandidos=16 (antes: crash) |
| A*+h=0 en `FoodSearchProblem`/`testClassic` | costo=16, expandidos=2598 (antes: crash) |

Los números de nodos expandidos coinciden EXACTAMENTE con los de nuestra propia implementación en
todos los casos probados. Esto es una buena noticia para la unificación: significa que ambos
estilos de algoritmo (el nuestro, que poda antes de insertar; el suyo, que reabre nodos después)
llegan a los mismos resultados una vez arreglado el desempate, así que no debería haber conflicto
de números entre las dos versiones al unificar el informe final.

## Qué se dejó sin tocar (a propósito)

- `depthFirstSearch` y `breadthFirstSearch` siguen sin implementar (`util.raiseNotDefined()`).
  Ninguna de las 11 actividades de la guía las pide directamente, así que no se tocaron —
  decisión del compañero de Parte 1 si quiere completarlas o no.
- `SearchProblem`, `tinyMazeSearch`, `nullHeuristic`: sin cambios, tal como venían.

## Archivo entregado

`search_corregido.py` (en este mismo paquete) es la versión ya corregida, lista para reemplazar la
que mandó el compañero. Recomendación: que la revise y la use, o que aplique los mismos dos cambios
sobre su propia copia si prefiere mantener su archivo como "fuente de la verdad".

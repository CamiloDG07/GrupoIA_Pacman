# Sustentación — Actividad 4: A* sin información (h(n) = 0)

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se formalizó, con `experimentos/actividad4_astar_nulo.py` sobre `mediumClassic`, la comparación
UCS vs. A*+h(n)=0 que ya se había verificado (para 5 layouts) en la Actividad 3. Mismo costo (12) y
mismos nodos expandidos (69, número corregido tras el fix del desempate en la cola de prioridad —
ver Actividad 3) en ambos algoritmos. Guardado en `resultados/resultados.csv` con `actividad=4`.

## Partes críticas (repaso, ya vistas en Actividad 3)

- **`f(n) = g(n) + h(n)`**: con `h(n) = 0` para todo `n`, se reduce algebraicamente a `f(n) = g(n)`,
  que es la prioridad exacta de UCS. No hay ninguna otra diferencia de código entre ambos algoritmos.

## ¿Qué pasa si...?

- **¿Qué pasa si en vez de `nullHeuristic` uso una heurística que devuelve una constante distinta
  de cero para todos los estados (por ejemplo, siempre 5)?**
  El comportamiento seguiría siendo idéntico a UCS en cuanto al **orden de expansión** (porque
  sumar la misma constante a todas las prioridades no cambia su orden relativo), pero el costo
  final reportado por `problem.getCostOfActions` no cambiaría (se sigue calculando sobre las
  acciones reales, no sobre `f(n)`). Es un buen ejemplo para mostrar que lo que importa de una
  heurística es cómo varía entre estados, no su valor absoluto.
- **¿Qué pasa si mido el tiempo con `-q` desde `pacman.py` en vez de con `time.perf_counter()`
  directo sobre el problema?**
  Se obtienen los mismos costos y nodos expandidos (esas métricas no dependen de cómo se mida el
  tiempo), pero el tiempo en sí sería menos preciso, porque incluiría la sobrecarga de inicializar
  todo el motor gráfico/textual de Pac-Man, no solo la búsqueda.

## Preguntas trampa esperadas del profesor

1. **"Si A* con h=0 es igual a UCS, ¿para qué existe UCS como algoritmo aparte?"**
   Históricamente UCS (equivalente a Dijkstra) es anterior y más simple de explicar sin el
   concepto de heurística; en la práctica, si se tiene A* implementado, UCS es reemplazable por
   A*+`nullHeuristic` sin ninguna pérdida. Se mantiene como algoritmo aparte por claridad
   pedagógica y porque en problemas sin heurística natural (o donde diseñar una es costoso) es
   más simple no tener que pasar un argumento extra.
2. **"¿La igualdad de nodos expandidos se mantendría si hubiera empates de prioridad resueltos de
   forma distinta entre ambas llamadas?"**
   En esta implementación no debería, porque tanto UCS como A*+h=0 insertan las mismas
   prioridades numéricas (mismo `g(n)`, sin heurística que rompa empates de otra forma), así que
   ambos usan el mismo criterio de desempate implícito de `heapq` sobre tuplas `(prioridad, item)`.

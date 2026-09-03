# Sustentación — Actividad 5: A* con distancia Manhattan

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se ejecutó A* con `manhattanHeuristic` (ya provista, no se implementó nada nuevo) sobre
`mediumClassic`, comparándola contra UCS con `demo_actividad5()` (`pacman/searchAgents.py`,
`python searchAgents.py 5`): mismo costo
óptimo (12), pero A*+Manhattan expande 4.60x menos nodos (69 → 15; números corregidos tras el fix
del desempate en la cola de prioridad — ver Actividad 3). Guardado en `resultados/resultados.csv`
(actividad=5).

## Partes críticas (de la heurística, no del algoritmo)

- **`abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])`**: suma de diferencias absolutas por eje. Es
  literalmente la fórmula $h_M(n) = |x_n-x_g| + |y_n-y_g|$ de la guía.
- **No usa `problem.walls` para nada** — esa es la clave de por qué es admisible (ver pregunta de
  análisis en el informe): al ignorar las paredes nunca puede sobreestimar.

## ¿Qué pasa si...?

- **¿Qué pasa si multiplico la heurística por 2 (`return 2 * (abs(...) + abs(...))`)?**
  Dejaría de ser admisible en general: en un laberinto sin obstáculos entre `n` y la meta, el
  costo real es exactamente `h_M(n)`, así que `2*h_M(n)` sobreestimaría el doble. Eso podría hacer
  que A* deje de ser óptimo (podría reportar un camino subóptimo). Es un buen experimento para
  mostrar en vivo: correrlo y ver que a veces sigue dando el costo óptimo por casualidad del
  layout, pero no está garantizado.
- **¿Qué pasa si se corre sobre un layout con muchas paredes en zigzag entre inicio y meta
  (a diferencia de `mediumClassic`, que es relativamente abierto)?**
  Manhattan seguiría siendo admisible (nunca sobreestima), pero su ventaja sobre UCS sería menor,
  porque la diferencia entre la distancia en línea recta y el camino real (con muchos rodeos)
  sería más grande: la heurística "subestima mucho" y guía menos.
- **¿Qué pasa si el costo por movimiento no fuera 1 (como en `StayEastSearchAgent`, ya presente en
  `searchAgents.py`, con costo `0.5**x`)?**
  Manhattan dejaría de ser admisible en general, porque cuenta pasos, no costo; para que siga
  siendo una heurística válida habría que multiplicarla por el costo mínimo posible de un paso.

## Preguntas trampa esperadas del profesor

1. **"¿Por qué Manhattan es exacta (no solo una cota inferior) cuando no hay paredes entre el
   estado y la meta?"**
   Porque sin paredes, el camino más corto en una cuadrícula con movimientos ortogonales es
   exactamente recorrer la diferencia en x más la diferencia en y — no hay forma de hacerlo en
   menos pasos, y tampoco hace falta más (se puede recorrer primero todo el eje x y luego todo el
   eje y, por ejemplo).
2. **"¿La heurística Manhattan es consistente, no solo admisible?"**
   Sí: para cualquier sucesor `n'` de `n` (un paso ortogonal), `h_M(n)` y `h_M(n')` difieren en
   exactamente 1 (se acerca o se aleja una celda en un eje), y el costo del paso también es 1;
   entonces `h_M(n) <= costo(n,n') + h_M(n')` se cumple siempre con igualdad o con margen.
3. **"Si `mediumMaze` no mostró ninguna mejora con Manhattan (Actividad 3), ¿eso significa que la
   heurística está mal implementada?"**
   No: significa que ese layout específico no tiene bifurcaciones donde una heurística pueda
   aportar algo, no que la heurística sea incorrecta. La heurística sigue siendo admisible y
   consistente ahí también; simplemente no hay ninguna decisión que orientar.

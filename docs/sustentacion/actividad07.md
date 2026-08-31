# Sustentación — Actividad 7: Diseño del estado para CornersProblem

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se completaron `getStartState`, `isGoalState` y `getSuccessors` de `CornersProblem` en
`searchAgents.py`. Estado elegido: `(posición, esquinas_visitadas)`, con `esquinas_visitadas` una
tupla de 4 booleanos. Medido con `experimentos/actividad7_corners_estado.py` sobre `tinyCorners`:
UCS da costo=22, expandidos=295. Se verificó paso a paso que la solución realmente visita las 4
esquinas. También se descubrió y documentó que `mediumCorners` tiene el punto de partida en un
cuarto sellado sin salida (confirmado con `PositionSearchProblem`, código del profesor sin tocar).

## Partes críticas del código

- **La tupla de esquinas visitadas es inmutable** — cada sucesor crea una tupla NUEVA
  (`visited[:idx] + (True,) + visited[idx+1:]`) en vez de modificar la existente. Si se modificara
  en el lugar (por ejemplo con una lista y `visited[idx] = True`), todos los estados que comparten
  esa referencia (por ejemplo, distintos sucesores generados desde el mismo estado padre) se
  corromperían entre sí.
- **`isGoalState` solo mira la segunda mitad del estado** (`all(esquinasVisitadas)`), nunca la
  posición — la meta es "todas visitadas", sin importar dónde termine Pac-Man.
- **El orden de `self.corners` es fijo** (`(1,1)`, `(1,top)`, `(right,1)`, `(right,top)`) y se
  reutiliza como el orden de la tupla de booleanos — por eso `self.corners.index(nextPosition)` da
  siempre el índice correcto para marcar esa esquina específica.

## ¿Qué pasa si...?

- **¿Qué pasa si el estado fuera solo la posición (sin las esquinas visitadas)?**
  El algoritmo terminaría (siempre reduce el problema a un espacio finito), pero podría fallar en
  encontrar la solución óptima, o incluso cualquier solución: al llegar dos veces a la misma
  posición con distinto progreso, un diccionario de "mejor costo conocido" (como el que usa
  `uniformCostSearch`) confundiría ambos casos y podría descartar como "ya visto, no mejora" un
  estado que en realidad todavía necesitaba explorarse porque le faltaban esquinas por visitar.
- **¿Qué pasa si se usa una lista en vez de una tupla para las esquinas visitadas?**
  El código fallaría al intentar usar ese estado como llave de un diccionario o dentro de
  `util.PriorityQueue` (las listas no son hasheables en Python), o peor: si de alguna forma
  funcionara sin dar error inmediato, distintos estados podrían terminar compartiendo/mutando la
  misma lista por referencia, corrompiendo la búsqueda silenciosamente.
- **¿Qué pasa si `mediumCorners` se usa de todos modos como layout de prueba?**
  UCS (o cualquier algoritmo, con cualquier heurística) devuelve una lista de acciones vacía: no es
  un bug de nuestra implementación, es que el punto de partida de Pac-Man en ese layout está
  encerrado sin salida. Se confirmó con el propio `PositionSearchProblem` del profesor.

## Preguntas trampa esperadas del profesor

1. **"¿Por qué no usaron un `set` de esquinas visitadas en vez de una tupla de booleanos de
   longitud fija?"**
   Un `set` de posiciones también sería hasheable (si se usa `frozenset`), pero la tupla de 4
   booleanos en un orden fijo es más simple y ligeramente más eficiente para un número fijo y
   pequeño de esquinas (siempre 4): comparar dos tuplas de 4 booleanos es más directo que comparar
   dos `frozenset`s de posiciones.
2. **"Si aumentara el número de esquinas a visitar (por ejemplo, 6 en vez de 4), ¿cambiaría el
   diseño del estado?"**
   No cambiaría la idea (posición + progreso), solo el tamaño de la tupla de booleanos (o se podría
   usar una máscara de bits/entero en vez de una tupla, para representar el mismo progreso de forma
   más compacta si el número de puntos a visitar creciera mucho).
3. **"¿Cómo se dieron cuenta de que `mediumCorners` estaba sellado, y no que su código tenía un
   bug?"**
   Se probó el mismo layout con `PositionSearchProblem`, que es código ya implementado por el
   profesor y no se tocó en ningún momento; como esa búsqueda independiente también falla en
   encontrar cualquier camino fuera del punto de partida, se descarta que el problema esté en nuestra
   implementación de `CornersProblem` específicamente.

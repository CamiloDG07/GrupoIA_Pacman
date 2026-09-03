# Sustentación — Actividad 6: Distancia Euclidiana y comparación de heurísticas

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se ejecutó A* con `euclideanHeuristic` (ya provista) y se comparó contra `nullHeuristic` y
`manhattanHeuristic` sobre `mediumClassic` con `demo_actividad6()` (`pacman/searchAgents.py`,
`python searchAgents.py 6`): mismo
costo óptimo (12) en las tres, pero Manhattan expande 15 nodos, Euclidiana 16 y h=0 expande 69
(números corregidos tras el fix del desempate en la cola de prioridad — ver Actividad 3). Guardado
en `resultados/resultados.csv` (actividad=6).

## Partes críticas

- **`((xy1[0]-xy2[0])**2 + (xy1[1]-xy2[1])**2) ** 0.5`**: la fórmula de distancia euclidiana
  estándar, sin ninguna adaptación al hecho de que Pac-Man se mueve en cuadrícula. Esa es
  justamente la raíz de por qué es menos informativa que Manhattan aquí.
- **Ambas heurísticas ignoran `problem.walls`**: por eso ambas son admisibles, pero por la misma
  razón ambas pueden desperdiciar información sobre el layout real.

## ¿Qué pasa si...?

- **¿Qué pasa si el problema permitiera movimiento diagonal (8 direcciones en vez de 4)?**
  Ahí Euclidiana sería la heurística más ajustada (más informativa que Manhattan), porque el
  costo real de moverse en diagonal se parecería más a la distancia en línea recta que a la suma
  de catetos. Este es un buen ejemplo para mostrar que "cuál heurística es mejor" depende del
  espacio de acciones del problema, no es una propiedad absoluta de la heurística.
- **¿Qué pasa si comparamos Manhattan y Euclidiana en un layout con muchas menos bifurcaciones
  (como `mediumMaze`, Actividad 2-3)?**
  Ambas expanden exactamente lo mismo (32 nodos, igual que h=0): sin bifurcaciones no hay ninguna
  decisión que una heurística, por más informativa que sea, pueda influir.
- **¿Qué pasa si tomamos la heurística `max(manhattanHeuristic(...), euclideanHeuristic(...))`
  para cada estado?**
  Seguiría siendo admisible (el máximo de dos heurísticas admisibles es admisible, y de hecho más
  informativa que cualquiera de las dos por separado, porque siempre es al menos tan grande como
  la mejor de las dos, sin dejar de ser una cota inferior válida). Es una técnica real usada más
  adelante en `cornersHeuristic`/`foodHeuristic` (Actividades 8 y 11).

## Preguntas trampa esperadas del profesor

1. **"¿Por qué $h_E(n) \le h_M(n)$ siempre?"**
   Es la desigualdad triangular aplicada a un triángulo rectángulo de catetos
   $|x_n-x_g|$ y $|y_n-y_g|$: la hipotenusa (distancia euclidiana) nunca es mayor que la suma de
   los catetos (distancia Manhattan). Se puede mostrar con el caso extremo: si $x_n=x_g$ o
   $y_n=y_g$ (movimiento en un solo eje), ambas distancias son iguales; en cualquier otro caso,
   Euclidiana es estrictamente menor.
2. **"Si Euclidiana subestima más, ¿por qué no es simplemente una mala heurística? ¿No sigue
   siendo admisible?"**
   Sigue siendo admisible y sigue garantizando que A* encuentre el costo óptimo; solo es menos
   *informativa*: admisibilidad garantiza correctitud, no eficiencia. Aportar menos información
   no es un error, es una heurística subóptima en cuanto a poda, no en cuanto a corrección.
3. **"¿Una heurística más grande (más cercana al costo real) siempre expande menos nodos?"**
   En general sí, siempre que se mantenga admisible: mientras más informativa (más cerca de
   $h^*(n)$ sin pasarse), menos nodos "de más" expande A*. Esto se vuelve el hilo conductor de la
   Actividad 11 (parte de la pregunta 6 del Análisis final de la guía).

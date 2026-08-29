# Sustentación — Actividad 1: Exploración del entorno

> Uso interno del grupo. No se entrega al profesor; es material de preparación para la exposición.

## Qué se hizo
Se ejecutó `pacman.py` manualmente y, además, se escribió `experimentos/actividad1_exploracion.py`,
que instancia `PositionSearchProblem` (ya provisto en `searchAgents.py`) y muestra en consola cada
componente del problema de búsqueda: estado, estado inicial, acciones, función sucesor, objetivo y costo.
No se modificó ningún algoritmo todavía.

## Partes críticas del código (para poder explicarlas en vivo)

- **`PositionSearchProblem.__init__`** (`searchAgents.py`, ~línea 120-160): recibe el `GameState` y
  guarda `self.walls`, `self.startState` y `self.goal` (por defecto `(1,1)`, salvo que se pase `goal`
  explícito). Si el profesor pregunta "¿de dónde sale el objetivo?", la respuesta está aquí.
- **`getSuccessors(state)`**: recorre las 4 direcciones cardinales, usa `Actions.directionToVector` para
  calcular la celda vecina y filtra con `self.walls[nextx][nexty]`. Es el corazón de la función de
  transición `T` del problema formal `P = (S, A, T, s0, G, C)`.
- **`self._expanded`**: contador que se incrementa cada vez que se llama `getSuccessors`; es la métrica
  de "nodos expandidos" que se usará desde la Actividad 2 en adelante.

## ¿Qué pasa si...?

- **¿Qué pasa si cambio el layout de `tinyMaze` a `mediumClassic`?**
  Cambia `s0` (posición inicial) y el tamaño del laberinto, pero la estructura del problema
  (`S, A, T, G, C`) es exactamente la misma: solo cambian los valores, no las reglas. Se puede
  demostrar corriendo `python experimentos/actividad1_exploracion.py mediumClassic`.
- **¿Qué pasa si Pac-Man arranca pegado a una esquina o pared?**
  `getSuccessors` simplemente devuelve menos de 4 sucesores (algunas direcciones quedan bloqueadas
  por `self.walls`); el problema sigue bien definido, solo con menor factor de ramificación en ese nodo.
- **¿Qué pasa si se le pasa un `goal` distinto al construir `PositionSearchProblem`?**
  `isGoalState` cambia de objetivo sin tocar nada más: es la misma idea que se reutiliza en
  `AnyFoodSearchProblem` más adelante en el proyecto.

## Preguntas trampa esperadas del profesor

1. **"¿El estado incluye la orientación de Pac-Man o los fantasmas?"**
   No. En `PositionSearchProblem` el estado es solo `(x, y)`; no incluye fantasmas ni orientación.
   Eso es justamente lo que se vuelve insuficiente en las Actividades 7 y 10 (esquinas y comida), donde
   el estado tiene que crecer para no perder información necesaria.
2. **"¿Por qué el costo es siempre 1 y no la distancia real recorrida?"**
   Porque en esta formulación cada acción es un paso de una celda de la cuadrícula; el costo modela
   "número de movimientos", no distancia euclidiana. Esto es una elección de diseño del problema, no
   una limitación del algoritmo de búsqueda.
3. **"Si dos estudiantes ejecutan el mismo layout, ¿deberían obtener el mismo estado inicial?"**
   Sí, siempre que usen el mismo archivo `.lay`: el estado inicial se lee directamente del layout
   (posición marcada con `P`), no es aleatorio.

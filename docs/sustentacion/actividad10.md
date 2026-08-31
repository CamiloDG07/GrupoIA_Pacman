# Sustentación — Actividad 10: FoodSearchProblem (línea base)

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
`FoodSearchProblem` ya viene implementado por el profesor; no se escribió código nuevo. Se corrió
UCS y A*+h(n)=0 sobre `tinySearch` (1 alimento) y `testClassic` (8 alimentos) con
`experimentos/actividad10_food_baseline.py`, confirmando que ambos coinciden en costo y nodos
expandidos (igual que en la Actividad 4). Se intentó adicionalmente UCS sobre `smallClassic`
(55 alimentos) con límite de 45s y no terminó — confirma la explosión combinatoria 2^F.

## Partes críticas del código (ya dadas, solo para entender)

- **El estado es `(pacmanPosition, foodGrid)`, no solo la posición** — por eso el `TypeError` que
  encontramos al preparar esta actividad (ver Actividad 3, sección de corrección): el `foodGrid` es
  un objeto `Grid`, no comparable, y eso rompía `heapq` en empates de prioridad antes del fix del
  contador de desempate.
- **`isGoalState` revisa `state[1].count() == 0`** — la meta no depende de la posición de Pac-Man en
  absoluto, solo de que no quede comida.
- **`getSuccessors` copia el grid de comida en cada sucesor (`nextFood = state[1].copy()`)** — cada
  estado sucesor tiene su propia copia del grid con un alimento menos si Pac-Man pasa por una celda
  con comida; esto es lo que hace que el espacio de estados explote (cada combinación distinta de
  comida restante es un estado distinto, aunque la posición sea la misma).

## ¿Qué pasa si...?

- **¿Qué pasa si Pac-Man pasa por una celda con comida pero el algoritmo de búsqueda "cree" que no
  hay comida ahí (por un bug al copiar el grid)?**
  El costo devuelto por `getCostOfActions` seguiría siendo correcto (cuenta pasos, no comida), pero
  `isGoalState` podría fallar en detectar la meta correctamente, o peor: reportar una meta falsa
  antes de haber recogido toda la comida real. Es un buen ejemplo de por qué `nextFood.copy()` es
  necesario en cada sucesor (sin copia, todos los estados compartirían el mismo objeto `Grid` y se
  corromperían entre sí).
- **¿Qué pasa si en vez de `testClassic` (8 alimentos) usamos un layout con 20-30 alimentos?**
  UCS y A*+h(n)=0 seguirían siendo correctos, pero el tiempo/nodos expandidos crecería mucho más
  rápido que linealmente respecto al número de alimentos (crecimiento exponencial, no lineal). Con
  55 alimentos (`smallClassic`) ya no terminó en 45 segundos.

## Preguntas trampa esperadas del profesor

1. **"¿Por qué el espacio de estados de este problema es mucho más grande que el de
   `PositionSearchProblem` o incluso `CornersProblem`?"**
   Porque el estado ya no es solo la posición (ni posición + 4 bits de esquinas visitadas, como en
   `CornersProblem`): incluye una configuración completa de qué alimentos quedan, que puede tomar
   hasta $2^F$ valores distintos para $F$ alimentos. Con solo 8 alimentos ya se expandieron 2598
   nodos con h=0; con 55 alimentos, UCS ni siquiera terminó en 45 segundos.
2. **"¿Por qué UCS y A*+h(n)=0 siguen coincidiendo exactamente aquí, igual que en la Actividad 4?"**
   Porque la igualdad $f(n) = g(n) + 0 = g(n)$ no depende de qué tan grande o complejo sea el
   estado: es una consecuencia algebraica de la fórmula de A*, válida para cualquier
   `SearchProblem`, incluido este.
3. **"¿`FoodSearchProblem` garantiza que la solución encontrada por UCS es óptima?"**
   Sí, por la misma razón que en cualquier problema con costo uniforme por paso: UCS explora en
   orden no decreciente de costo acumulado, así que la primera meta que encuentra es,
   necesariamente, la de menor costo.

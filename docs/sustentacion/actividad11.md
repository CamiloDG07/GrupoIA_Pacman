# Sustentación — Actividad 11: Diseño de `foodHeuristic` (dos versiones + caché)

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se implementaron dos heurísticas para `FoodSearchProblem` en `searchAgents.py`:
- `foodHeuristicV1` (Heurística 1): distancia Manhattan al alimento más lejano, la fórmula exacta
  que sugiere la guía.
- `foodHeuristic` (Heurística 2, la que usa `AStarFoodSearchAgent`): diámetro Manhattan del
  conjunto {posición actual} ∪ {alimentos restantes}, con caché de las distancias entre pares de
  alimentos en `problem.heuristicInfo`.

Comparadas en `testClassic` (8 alimentos): h=0 expande 2598 nodos, Heurística 1 expande 702,
Heurística 2 expande 383 — mismo costo óptimo (16) en las tres. Se comparó además el tiempo con y
sin caché (`foodHeuristicV2SinCache`) en `testClassic` y `capsuleClassic` (23 alimentos): en ambos
casos, la versión SIN caché fue ligeramente más rápida (4-7%), un resultado honesto que se explica
y documenta en el informe (ver sección dedicada en `actividad11_food_heuristic.tex`).

## Partes críticas del código

- **`if not foodList: return 0`** — caso base necesario: sin esto, `max()` sobre una lista vacía
  (el estado meta, donde ya no queda comida) lanzaría `ValueError`.
- **El caché se guarda con `problem.start[1].asList()`, no con `foodGrid.asList()` del estado
  actual** — es clave usar las posiciones de comida del estado INICIAL del problema (que nunca
  cambian) para precalcular todas las distancias entre pares una sola vez; usar el `foodGrid` del
  estado actual recalcularía el caché cada vez que cambia el conjunto de comida restante, perdiendo
  todo el sentido de cachear.
- **La clave del diccionario es la posición `(x,y)` del alimento, no un índice** — así el mismo
  diccionario sirve para consultar la distancia entre cualquier par de alimentos que sigan
  presentes en cualquier estado posterior, sin importar en qué orden aparezcan en `foodGrid.asList()`
  en ese momento.

## ¿Qué pasa si...?

- **¿Qué pasa si la heurística no considerara los pares de alimentos entre sí (solo la Heurística 1)?**
  Seguiría siendo admisible y consistente, pero menos informativa: en `testClassic` expande casi el
  doble de nodos que la Heurística 2 (702 vs. 383), porque ignora que visitar dos alimentos lejanos
  entre sí también tiene un costo mínimo, independiente de dónde esté Pac-Man.
- **¿Qué pasa si en vez de Manhattan usáramos la distancia real de laberinto (`mazeDistance`, ya
  provista) para el diámetro?**
  Sería una heurística aún más informativa (más cercana al costo real, porque `mazeDistance` sí
  considera las paredes), y ahí el caché probablemente SÍ mostraría un beneficio medible, porque
  `mazeDistance` internamente corre un BFS completo --mucho más costoso que una resta de enteros--.
  No se implementó porque requiere `breadthFirstSearch` en `search.py` (hoy vacío, y ese archivo lo
  está tomando un compañero); queda documentado como la extensión natural si se quisiera una
  Heurística 3.
- **¿Qué pasa si el caché se llenara con información que sí cambia entre estados (por ejemplo, la
  posición de Pac-Man)?**
  Sería un error grave: el caché asume implícitamente que lo que guarda es constante durante toda
  la búsqueda. Guardar algo que cambia produciría valores de heurística incorrectos (potencialmente
  inconsistente o inadmisible), rompiendo la garantía de optimalidad de A*.

## Preguntas trampa esperadas del profesor

1. **"Implementaron un caché con `problem.heuristicInfo` pero no mejoró el tiempo. ¿Entonces el
   caché no sirve?"**
   El caché en sí es correcto y es la herramienta que pide la guía; lo que pasa es que, en este
   caso concreto, el cálculo cacheado (una resta de enteros) es más barato que el costo de
   consultarlo (construir una tupla y calcular su hash). El caché ayuda cuando lo que se evita
   recalcular es genuinamente costoso --como una búsqueda BFS completa (`mazeDistance`)--, no
   cuando es aritmética trivial. Es una lección real de ingeniería de software, no un error nuestro.
2. **"¿Por qué la Heurística 2 expande menos nodos que la Heurística 1 si ambas son admisibles?"**
   Porque admisibilidad solo garantiza optimalidad (nunca sobreestima), no dice nada sobre qué tan
   *informativa* es la heurística. La Heurística 2 domina a la Heurística 1 en el sentido de que
   $h_2(n) \ge h_1(n)$ para todo $n$ (el diámetro de un conjunto siempre es al menos tan grande como
   la distancia de un punto específico a otro punto del conjunto), así que Heurística 2 nunca es
   menos informativa, y en `testClassic` es estrictamente más informativa.
3. **"¿Podrían diseñar una Heurística 3 todavía mejor?"**
   Sí: usando `mazeDistance` (distancia real de laberinto vía BFS) en vez de Manhattan para el
   diámetro, sería más ajustada al costo real (nunca subestimaría tanto como Manhattan cuando hay
   paredes de por medio) y ahí el caché sí mostraría beneficio real, porque evitaría repetir un BFS
   completo. No se implementó en esta entrega porque requiere completar `breadthFirstSearch` en
   `search.py`, archivo que en este grupo lo está trabajando un compañero (Parte 1); queda anotado
   como una extensión posible.

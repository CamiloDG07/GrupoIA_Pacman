# Sustentación — Actividad 8: Heurísticas para CornersProblem

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se implementaron dos heurísticas en `searchAgents.py`: `cornersHeuristicBasica` (fórmula de la
guía: distancia Manhattan a la esquina pendiente más lejana) y `cornersHeuristic` (la que usa
`AStarCornersAgent` — diámetro Manhattan de {posición} ∪ {esquinas pendientes}, mismo patrón que
`foodHeuristic` de la Actividad 11). Sobre `tinyCorners`: h=0 expande 295, básica 147, propuesta
119 — las tres llegan al mismo costo óptimo (22).

## Partes críticas del código

- **`pendientes = [c for c, v in zip(corners, visited) if not v]`** — ambas heurísticas arrancan
  filtrando solo las esquinas que TODAVÍA no se visitaron; si `pendientes` está vacío (ya se
  visitaron las 4), la heurística devuelve `0` de inmediato (coincide con `isGoalState`).
- **La propuesta agrega la posición actual a la lista de puntos** (`puntos = [position] +
  pendientes`) antes de calcular el máximo de todas las distancias por pares — por eso siempre es
  ≥ que la básica (el término de la básica, `max distancia posición-esquina`, está incluido dentro
  de ese mismo máximo).
- **No se usó `problem.heuristicInfo` como caché aquí** — a diferencia de `foodHeuristic`, con
  máximo 4 esquinas (6 pares) el cálculo es tan barato que cachearlo no tendría sentido (mismo
  hallazgo que en la Actividad 11, pero aquí ni se intentó porque ya sabíamos que no compensaría).

## ¿Qué pasa si...?

- **¿Qué pasa si se usa la heurística básica en vez de la propuesta en `AStarCornersAgent`?**
  Seguiría siendo admisible y consistente (se demuestra igual), y seguiría encontrando el costo
  óptimo (22), pero expandiría más nodos (147 en vez de 119) — sigue siendo correcta, solo menos
  eficiente.
- **¿Qué pasa si la heurística sobreestimara en algún estado?**
  A* podría devolver una solución subóptima (de costo mayor a 22) sin que nada en el código lo
  detecte — por eso la guía pide justificar por escrito la admisibilidad, no solo "que funcione en
  la práctica": encontrar el costo óptimo en un layout de prueba no prueba admisibilidad en
  general, solo la hace plausible.
- **¿Qué pasa si en vez de tomar el máximo se sumaran las distancias a cada esquina pendiente?**
  Dejaría de ser admisible: sumar sobreestimaría, porque un solo recorrido puede visitar varias
  esquinas usando tramos compartidos (no hay que recorrer la distancia completa hasta CADA esquina
  por separado desde la posición actual).

## Preguntas trampa esperadas del profesor

1. **"¿Por qué la heurística propuesta nunca es peor (nunca expande más) que la básica?"**
   Porque `h_propuesta(n) >= h_basica(n)` siempre (la propuesta incluye el mismo término más uno
   adicional), y una heurística más informada (mayor, sin dejar de ser admisible) nunca hace que
   A* explore más nodos que una menos informada — es una propiedad general de A*, no algo
   específico de este problema.
2. **"¿Por qué no compararon usando `problem.heuristicInfo` aquí, si sí ayudó (o no ayudó) en la
   Actividad 11?"**
   En la Actividad 11 SÍ se probó y el hallazgo fue que no ayudaba (la aritmética es más barata que
   la consulta al diccionario) en un problema con decenas de alimentos. Aquí, con máximo 4
   esquinas, el mismo razonamiento aplica con más fuerza todavía: el costo de calcular las
   distancias es aún menor, así que cachear definitivamente no compensaría.
3. **"Demuestre que su heurística es consistente, no solo admisible."**
   Ver la subsección de consistencia en `actividad08_corners_heuristica.tex`: se aplica la misma
   desigualdad triangular de Manhattan usada en la Actividad 11, ahora sobre {posición} ∪
   {esquinas pendientes} en vez de {posición} ∪ {comida restante}.

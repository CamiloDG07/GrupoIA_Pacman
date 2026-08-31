---
title: Cómo reemplazar los pantallazos del informe
---

# Qué hacer con esta carpeta

Cada imagen `.png` de esta carpeta es un **placeholder** (marcador temporal)
que el informe (`informe.pdf`) ya usa mediante `\includegraphics`. Para que
el informe muestre tu captura real de VS Code en vez del recuadro rojo de
"PANTALLAZO PENDIENTE", solo tienes que:

1. Abrir en VS Code el archivo y las líneas indicadas en el propio
   placeholder (también están en la tabla de abajo).
2. Tomar el pantallazo (recomendado: seleccionar solo esas líneas para que
   se vea el resaltado de sintaxis, y que el número de línea sea visible).
3. Guardar la captura **con el mismo nombre de archivo** que ya tiene el
   placeholder (por ejemplo `actividad02_ucs.png`), reemplazando el archivo
   existente en esta carpeta.
4. Recompilar el informe (`pdflatex informe.tex`, dos veces). No hay que
   tocar el `.tex` de nuevo: el `\includegraphics` ya apunta a ese nombre.

No es necesario reemplazar los 10; puedes ir haciéndolo de a poco y
recompilar cada vez para ver el avance.

## Tabla de pantallazos pendientes

| Archivo de imagen | Screenshot de... | Archivo real | Líneas |
|---|---|---|---|
| `actividad02_ucs.png` | `uniformCostSearch` | `pacman/search.py` | 111-142 |
| `actividad03_astar.png` | `aStarSearch` | `pacman/search.py` | 178-211 |
| `actividad05_manhattan.png` | `manhattanHeuristic` | `pacman/searchAgents.py` | 236-240 |
| `actividad06_euclidiana.png` | `euclideanHeuristic` | `pacman/searchAgents.py` | 242-246 |
| `actividad07_corners.png` | `getStartState`/`isGoalState`/`getSuccessors` de `CornersProblem` | `pacman/searchAgents.py` | 273-351 |
| `actividad08_heuristica_basica.png` | `cornersHeuristicBasica` | `pacman/searchAgents.py` | 367-396 |
| `actividad08_heuristica_propuesta.png` | `cornersHeuristic` | `pacman/searchAgents.py` | 399-452 |
| `actividad10_food_isgoal.png` | `FoodSearchProblem.__init__`/`isGoalState` | `pacman/searchAgents.py` | 460-480 |
| `actividad11_heuristica1.png` | `foodHeuristicV1` | `pacman/searchAgents.py` | 516-540 |
| `actividad11_heuristica2.png` | `foodHeuristic` (con caché) | `pacman/searchAgents.py` | 543-608 |

Para el detalle de **qué explicar de cada pantallazo** (qué hace, por qué se
hizo así, y cómo afecta a los resultados), ver `docs/guia_codigos_clave.md`
en la raíz del repo — es la misma guía que sirvió para escribir cada
sección del informe y sirve también para estudiar antes de la sustentación.

El script `_generar_placeholders.py` es el que generó estas imágenes; no
hace falta volver a correrlo a menos que quieras regenerar los placeholders
(por ejemplo si borras una captura real por error).

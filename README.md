# Taller de Búsqueda Informada con Pac-Man — Inteligencia Artificial (SIST5036)

**Universidad Sergio Arboleda** · Escuela de Ciencias Exactas e Ingeniería
**Grupo:** Camilo Díaz, Juan David, Mario
**Guía de referencia:** `Taller_Busqueda_Informada.pdf` (Algoritmo A*, heurísticas, distancia Manhattan y Euclidiana)

## 1. Regla de oro del proyecto

El motor de Pac-Man (`pacman/`) es el proporcionado por el profesor y **no se toca su arquitectura**.
Solo se completan las funciones marcadas como pendientes dentro de dos archivos:

- `pacman/search.py` → `uniformCostSearch`, `aStarSearch`
- `pacman/searchAgents.py` → `CornersProblem`, `cornersHeuristic`, `foodHeuristic`

Todo lo demás (clases de juego, gráficos, layouts) queda intacto. No se crea una "versión propia" del juego.

## 2. Por qué esta estructura de repositorio (y no un .py suelto por actividad)

`search.py` y `searchAgents.py` son archivos **compartidos**: UCS y A* viven en el mismo `search.py`,
y `CornersProblem`/`cornersHeuristic`/`foodHeuristic` viven en el mismo `searchAgents.py`. El propio
enunciado (página 16) exige entregar exactamente esos dos archivos dentro del zip `GrupoXX_Pacman_AStar.zip`.
Por eso **no se puede** partir la solución en un `.py` independiente por actividad sin romper el entregable
que pide el profesor.

La forma correcta de lograr lo que se busca (saber exactamente qué se cambió en cada actividad, y poder
explicarlo/mostrarlo en la sustentación) es combinar tres cosas:

1. **Un commit de Git por actividad**, con el código fuente de verdad viviendo solo en `pacman/`.
   `git log --oneline` y `git show <commit>` muestran, actividad por actividad, exactamente qué línea se
   agregó o cambió — mejor que mantener copias duplicadas del mismo archivo.
2. **Un script de experimento por actividad** en `experimentos/` (p. ej. `actividad5_manhattan.py`). Estos
   scripts NO reimplementan el algoritmo: importan `pacman/` y ejecutan/miden esa actividad puntual
   (nodos expandidos, costo, tiempo). Esto sí es un archivo aislado por actividad, y es justo lo que se
   muestra en la sustentación cuando el profesor pregunta "¿qué pasa si cambio X?" — se corre ese único
   script y se ve el efecto sin tocar el resto del proyecto.
3. **El informe LaTeX** (`docs/latex/`), con un archivo de sección por actividad
   (`docs/latex/secciones/actividadNN_*.tex`) que se van agregando al `informe.tex` maestro a medida que
   se avanza. Esto da documentación granular por actividad sin duplicar código.

Adicionalmente, `docs/sustentacion/actividadNN.md` guarda, por actividad, la preparación para la
exposición: qué parte del código es crítica, qué pasa si se modifica tal variable, y preguntas "trampa"
típicas — esto es material de estudio del grupo, no se entrega al profesor.

## 3. Estructura

```
GrupoIA_Pacman/
├── pacman/                     # Código base del profesor (search.py y searchAgents.py se completan aquí)
├── experimentos/                # Un script por actividad: ejecuta + mide, no reimplementa
├── resultados/
│   └── resultados.csv           # Tabla consolidada de métricas (todas las actividades)
├── docs/
│   ├── latex/
│   │   ├── informe.tex          # Documento maestro (portada, estructura institucional USA)
│   │   └── secciones/           # Una sección .tex por actividad, se agrega incrementalmente
│   └── sustentacion/            # Notas de preparación para la exposición (uso interno del grupo)
├── entregable/
│   └── empaquetar.sh            # Arma GrupoXX_Pacman_AStar.zip con la estructura exacta del enunciado
├── requirements.txt
└── .gitignore
```

## 3.1. Layout de referencia para comparar UCS y A*

Las Actividades 4, 5, 6 y 9 comparan UCS contra A* con distintas heurísticas sobre un mismo
laberinto. Se eligió **`mediumClassic`** como layout principal: tiene bifurcaciones reales, así
que las heurísticas sí muestran diferencia frente a UCS (69 nodos expandidos vs. 15 con
Manhattan). `mediumMaze` (usado inicialmente) se descartó como layout principal porque es un
pasillo sin bifurcaciones, y ninguna heurística cambia nada allí; se conserva como caso de
contraste en el informe.

> Nota: estos números fueron corregidos tras encontrar y arreglar un bug de desempate
> (*tie-breaking*) en la cola de prioridad de `search.py`, detectado al extender las pruebas a
> `FoodSearchProblem` (Actividad 11). No afecta ningún costo óptimo reportado, solo el conteo
> exacto de nodos expandidos — ver la sección correspondiente en `docs/latex/secciones/actividad03_astar.tex`.

> Nota sobre `informe.tex`: no incluye secciones separadas de "Introducción" ni "Objetivos" —
> el profesor indicó que esas secciones son solo para el proyecto final de la asignatura, no
> para los talleres/laboratorios. El informe de este taller empieza directamente en la
> Actividad 1.

## 4. Flujo de trabajo (uno por uno, actividad por actividad)

Para cada actividad:

1. Completar el código correspondiente en `pacman/search.py` o `pacman/searchAgents.py`.
2. Ejecutar el script de esa actividad en `experimentos/` y registrar sus métricas en `resultados/resultados.csv`.
3. Redactar `docs/latex/secciones/actividadNN_*.tex` con lo encontrado.
4. Escribir las notas de sustentación en `docs/sustentacion/actividadNN.md`.
5. `git add -A && git commit -m "Actividad N: <lo que se implementó>"`.
6. No se pasa a la siguiente actividad hasta confirmar que esta quedó entendida.

## 5. Cómo correr el proyecto

```bash
cd pacman
python pacman.py                              # jugar manualmente (flechas o W/A/S/D)
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l tinyCorners -p AStarCornersAgent -q     # sin gráficos, solo métricas
python pacman.py -l trickyClassic -p AStarFoodSearchAgent -q
```

`-q` corre sin la ventana gráfica (útil para medir tiempo/nodos rápido en cada experimento).

## 6. Entregable final para el profesor

El enunciado pide exactamente:

```
GrupoXX_Pacman_AStar.zip
├── search.py
├── searchAgents.py
├── resultados.csv
└── informe.pdf
```

`entregable/empaquetar.sh` genera ese zip a partir de `pacman/search.py`, `pacman/searchAgents.py`,
`resultados/resultados.csv` y el PDF compilado de `docs/latex/informe.tex`.

## 7. Sobre el repositorio de GitHub

Este mismo directorio es apto para subirse tal cual a un repositorio de GitHub (incluye `.gitignore` y
`requirements.txt`). Se recomienda repo privado con los tres integrantes como colaboradores, rama `main`
protegida, y un commit por actividad como se describe en la sección 4. El material de referencia de otro
grupo (documento adjunto) **no se incluye** en este repositorio: solo se usó para calibrar el nivel de
profundidad esperado en el informe.

## 8. Nota sobre el código base

El proyecto (`pacman.py`, `search.py`, `searchAgents.py`, `util.py`, `game.py`, etc.) corresponde a la
adaptación clásica de Berkeley/Stanford CS221 usada en la guía de laboratorio. Se conserva sin cambios de
arquitectura, tal como lo exige el enunciado.

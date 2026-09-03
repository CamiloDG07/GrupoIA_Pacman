# Taller de Búsqueda Informada con Pac-Man — Inteligencia Artificial (SIST5036)

**Universidad Sergio Arboleda** · Escuela de Ciencias Exactas e Ingeniería
**Grupo 4:** Juan David Andradé Gómez, Mario Jiménez López, Camilo Andrés Díaz García
**Guía de referencia:** `Taller_Busqueda_Informada.pdf`

## 1. Qué es este proyecto

Este repositorio implementa el laboratorio de búsqueda informada sobre el entorno Pac-Man
(adaptación clásica de Berkeley/Stanford CS221): algoritmos de búsqueda no informada (UCS) e
informada (A*), diseño de heurísticas admisibles y consistentes, y dos problemas de búsqueda con
estado extendido (recorrer las cuatro esquinas del laberinto y recolectar toda la comida).

El repositorio contiene únicamente el entregable final para el profesor: el código de los
algoritmos, la tabla de métricas experimentales, y el informe técnico en PDF.

## 2. Estructura del repositorio

```
GrupoIA_Pacman/
├── informe.pdf              # Informe tecnico compilado, documenta cada actividad
├── pacman/
│   ├── search.py            # uniformCostSearch, aStarSearch
│   └── searchAgents.py      # CornersProblem, cornersHeuristic, FoodSearchProblem, foodHeuristic,
│                             #   AStarCornersAgent, AStarFoodSearchAgent, y demo_actividad1..11
│                             #   (reproducen los datos de cada actividad; ver seccion 4)
├── resultados/
│   └── resultados.csv       # Datos experimentales citados en el informe: actividad, metodo,
│                             #   layout, costo, nodos expandidos, memoria (nodos y bytes), tiempo
├── entregable/
│   ├── empaquetar.sh        # Genera el zip final con la estructura exacta que exige el enunciado
│   └── Grupo04_Pacman_AStar.zip
├── requirements.txt
└── .gitignore
```

`search.py` y `searchAgents.py` son el motor de búsqueda del taller; el proyecto base de Pac-Man
del profesor (`pacman.py`, `game.py`, `util.py`, `layout.py`, `layouts/`, etc.) no se incluye aquí
porque no forma parte del entregable — el enunciado indica que el profesor ya cuenta con esos
archivos.

## 3. Cómo correr el código

Estos dos archivos están pensados para copiarse sobre el proyecto base de Pac-Man del profesor.
Colocados ahí (junto a `pacman.py`, `game.py`, `util.py`, `layout.py` y `layouts/`), dentro de esa
carpeta:

```bash
# Reproducir los datos de una actividad puntual
python searchAgents.py N        # N de 1 a 11, o "generales" para la tabla consolidada

# Ver un algoritmo resolver el laberinto graficamente
python pacman.py -l mediumClassic -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l tinyCorners -p AStarCornersAgent
python pacman.py -l testClassic -p AStarFoodSearchAgent
```

Cada `demo_actividadN()` imprime sus resultados en la terminal y agrega una fila a un
`resultados.csv` en el directorio desde el que se corre.

## 4. Entregable final para el profesor

El enunciado exige exactamente:

```
Grupo04_Pacman_AStar.zip
├── search.py
├── searchAgents.py
├── resultados.csv
└── informe.pdf
```

(archivos sueltos en la raíz del zip, sin subcarpeta contenedora.)

`entregable/empaquetar.sh Grupo04` genera ese zip automáticamente a partir de
`pacman/search.py`, `pacman/searchAgents.py`, `resultados/resultados.csv` e `informe.pdf`. Cada vez
que se actualiza el código o el informe, se vuelve a correr ese script para regenerar el zip.

## 5. Requisitos

- **Python 3.10 o superior** (los algoritmos solo usan la librería estándar).
- Dependencias opcionales: `pip install -r requirements.txt`.

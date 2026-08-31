# Taller de Búsqueda Informada con Pac-Man — Inteligencia Artificial (SIST5036)

**Universidad Sergio Arboleda** · Escuela de Ciencias Exactas e Ingeniería
**Grupo 4:** Juan David Andradé Gómez, Mario Jiménez López, Camilo Andrés Díaz García
**Guía de referencia:** `Taller_Busqueda_Informada.pdf`

## 1. Qué es este proyecto

Este repositorio implementa y documenta el laboratorio de búsqueda informada sobre el entorno
Pac-Man (adaptación clásica de Berkeley/Stanford CS221): algoritmos de búsqueda no informada
(UCS) e informada (A*), diseño de heurísticas admisibles y consistentes, y dos problemas de
búsqueda con estado extendido (recorrer las cuatro esquinas del laberinto y recolectar toda la
comida). El resultado son tres entregables: el código de los algoritmos, una tabla de métricas
experimentales, y un informe técnico en LaTeX que documenta cada actividad.

El proyecto está organizado para que cualquiera de los tres integrantes —o un tercero, como el
profesor— pueda entender qué se implementó, dónde vive cada pieza, y por qué se tomó cada
decisión de diseño, sin depender de que se lo expliquen verbalmente.

## 2. Regla de oro

El motor de Pac-Man (`pacman/`) es el proporcionado por el profesor y **no se modifica su
arquitectura**. El trabajo del grupo se limita a completar las funciones marcadas como
pendientes, en exactamente dos archivos:

- `pacman/search.py` → `uniformCostSearch`, `aStarSearch`
- `pacman/searchAgents.py` → `CornersProblem`, `cornersHeuristic`, `foodHeuristic`

Todo lo demás (interfaz gráfica, motor del juego, formato de los layouts) queda intacto.

## 3. Estructura del repositorio, archivo por archivo

```
GrupoIA_Pacman/
├── pacman/
│   ├── search.py           # Algoritmos de busqueda: uniformCostSearch y aStarSearch (implementados por el grupo)
│   ├── searchAgents.py     # Definicion de problemas y heuristicas: CornersProblem, cornersHeuristic,
│   │                       #   FoodSearchProblem, foodHeuristic (implementados por el grupo), mas los
│   │                       #   agentes ya armados AStarCornersAgent / AStarFoodSearchAgent
│   ├── pacman.py           # Motor principal del juego (codigo del profesor, no se toca)
│   ├── game.py             # Reglas del juego y logica de estado (codigo del profesor)
│   ├── util.py             # Estructuras de datos auxiliares: PriorityQueue, Stack, Queue (codigo del profesor)
│   ├── graphicsDisplay.py, graphicsUtils.py, textDisplay.py   # Interfaz grafica/consola (codigo del profesor)
│   ├── ghostAgents.py, keyboardAgents.py, sanityAgents.py     # Agentes auxiliares (codigo del profesor)
│   ├── layout.py           # Carga los archivos .lay y calcula coordenadas (codigo del profesor)
│   └── layouts/*.lay       # Mapas/laberintos de prueba (tinyMaze, mediumClassic, tinyCorners, etc.)
│
├── experimentos/
│   └── actividadN_*.py     # Un script por actividad. Cada uno importa pacman/ y ejecuta el algoritmo
│                            #   correspondiente sobre un layout concreto, midiendo nodos expandidos, costo
│                            #   y tiempo. No reimplementan nada: son el instrumento de medicion, no la solucion.
│                            #   Cada corrida agrega una fila a resultados/resultados.csv.
│
├── resultados/
│   └── resultados.csv      # Tabla consolidada: una fila por corrida de experimento, con las columnas
│                            #   actividad, metodo, layout, costo, nodos expandidos y tiempo. Es la fuente
│                            #   de todos los numeros citados en el informe.
│
├── docs/
│   └── latex/
│       ├── informe.tex     # Documento maestro: portada, tabla de contenido, bibliografia. Enlaza
│       │                   #   (\input) cada seccion en el orden en que se leen.
│       ├── secciones/
│       │   └── actividadNN_*.tex   # Una seccion por actividad: procedimiento, resultados, tabla y
│       │                            #   analisis. Se agregan incrementalmente sin tocar informe.tex.
│       ├── capturas/*.png  # Pantallazos de codigo referenciados desde las secciones
│       └── informe.pdf     # PDF compilado, listo para el entregable
│
├── entregable/
│   ├── empaquetar.sh       # Genera el zip final con la estructura exacta que exige el enunciado
│   └── Grupo04_Pacman_AStar.zip   # Entregable final (se regenera con empaquetar.sh, no se edita a mano)
│
├── requirements.txt        # Dependencias de Python (ver seccion 5)
└── .gitignore
```

## 4. Por qué esta organización

`search.py` y `searchAgents.py` son archivos **compartidos**: todos los algoritmos y heurísticas
del taller viven en esos mismos dos archivos, porque así lo exige el enunciado (página 16) para
el zip de entrega. Esto significa que no es posible tener un `.py` independiente por actividad sin
romper esa estructura.

La forma de conservar trazabilidad —saber exactamente qué se implementó en cada actividad, y
poder explicarlo en la sustentación— es a través de tres mecanismos independientes, en vez de
duplicar código:

1. **Un commit de Git por actividad.** `git log --oneline` y `git show <commit>` muestran,
   actividad por actividad, qué línea se agregó o modificó en el código fuente único.
2. **Un script de experimento por actividad**, en `experimentos/`. Sirve como evidencia
   reproducible y como demostración en vivo: ante una pregunta del tipo "¿qué pasa si cambio X?",
   se corre ese único script y se observa el efecto sin tocar el resto del proyecto.
3. **Una sección de informe por actividad**, en `docs/latex/secciones/`. Documenta de forma
   granular el procedimiento, los resultados y el análisis de cada punto, sin duplicar el código
   que ya vive en `pacman/`.

Bajo este esquema, el reparto de trabajo entre los tres integrantes queda registrado de forma
natural en el historial de commits (`git log --oneline`), sin necesidad de carpetas separadas por
persona.

### Layout de referencia para comparar UCS y A*

Las actividades que comparan UCS contra A* con distintas heurísticas usan **`mediumClassic`**
como layout principal: al tener bifurcaciones reales, permite que las heurísticas muestren una
diferencia medible frente a UCS. `mediumMaze` se usa como caso de contraste: al ser un pasillo sin
bifurcaciones, ninguna heurística cambia el resultado allí, lo cual es en sí mismo un hallazgo
relevante sobre cuándo una heurística aporta valor.

### Alcance del informe

`informe.tex` no incluye secciones separadas de "Introducción" ni "Objetivos": esas secciones
aplican solo al proyecto final de la asignatura, según indicación del profesor. El informe de este
taller comienza directamente en la Actividad 1.

## 5. Requisitos e instalación

Para trabajar en este proyecto (correr el código, ver el Pac-Man gráfico, o compilar el informe)
cada integrante necesita:

**Software base:**
- **Python 3.10 o superior** (el proyecto no usa librerías externas para los algoritmos; solo la
  librería estándar). Verificar con `python --version`.
- **Git**, para clonar el repositorio y sincronizar cambios.
- **Visual Studio Code** (recomendado, no obligatorio).

**Dependencias de Python** — instalar con:
```bash
pip install -r requirements.txt
```
(Solo incluye `matplotlib`, opcional, para gráficas auxiliares fuera del informe. Los algoritmos
en sí no requieren ninguna dependencia externa.)

**Para compilar el informe (`docs/latex/informe.tex`) y ver el PDF actualizarse en VS Code:**
- Extensión de VS Code **"LaTeX Workshop"** (de James Yu) — da un botón de compilar y una vista
  previa del PDF en un panel dividido dentro de VS Code, similar a Overleaf.
- Una distribución de LaTeX instalada en el sistema operativo (la extensión no la incluye):
  - Windows: **MiKTeX** — https://miktex.org/download
  - macOS: **MacTeX** — https://tug.org/mactex/
  - Linux: paquete `texlive-full` del gestor de paquetes de la distribución.

Sin la distribución de LaTeX instalada, la extensión se instala pero no puede compilar.

## 6. Cómo ejecutar el proyecto

Todos los comandos siguientes se ejecutan desde una terminal, parado dentro de la carpeta
`pacman/`:

```bash
cd pacman

# Jugar manualmente (flechas de direccion o W/A/S/D)
python pacman.py -l tinyMaze

# Ver un algoritmo resolver el laberinto automaticamente
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumClassic -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

# Problemas con estado extendido (esquinas y comida)
python pacman.py -l tinyCorners -p AStarCornersAgent
python pacman.py -l testClassic -p AStarFoodSearchAgent
```

Para generar los datos que van al informe, desde la **raíz** del proyecto (no desde `pacman/`):

```bash
python experimentos/actividad1_exploracion.py
python experimentos/actividad2_ucs.py
# ... un script por actividad, ver experimentos/
```

Cada script imprime sus resultados en la terminal y agrega una fila a `resultados/resultados.csv`.

Para compilar el informe manualmente (sin la extensión de VS Code):

```bash
cd docs/latex
pdflatex informe.tex
pdflatex informe.tex   # se corre dos veces para resolver el indice y las referencias cruzadas
```

## 7. Flujo de trabajo por actividad

1. Completar el código correspondiente en `pacman/search.py` o `pacman/searchAgents.py`.
2. Ejecutar el script de esa actividad en `experimentos/` y verificar que la fila se agregó a
   `resultados/resultados.csv`.
3. Redactar la sección correspondiente en `docs/latex/secciones/actividadNN_*.tex`.
4. `git add -A && git commit -m "Actividad N: <lo que se implementó>"`.

## 8. Entregable final para el profesor

El enunciado exige exactamente:

```
Grupo04_Pacman_AStar.zip
├── search.py
├── searchAgents.py
├── resultados.csv
└── informe.pdf
```

(archivos sueltos en la raíz del zip, sin subcarpeta contenedora, tal como lo muestra el
enunciado.)

`entregable/empaquetar.sh Grupo04` genera ese zip automáticamente a partir de
`pacman/search.py`, `pacman/searchAgents.py`, `resultados/resultados.csv` y el PDF compilado de
`docs/latex/informe.tex`. Cada vez que se actualiza el código o el informe, se vuelve a correr ese
script para regenerar el zip con la versión más reciente.

## 9. Sobre el repositorio de GitHub

Este directorio es apto para subirse tal cual a un repositorio de GitHub (incluye `.gitignore` y
`requirements.txt`). Se recomienda repositorio privado con los tres integrantes como
colaboradores y un commit por actividad, como se describe en la sección 7.

## 10. Sobre el código base

El proyecto (`pacman.py`, `search.py`, `searchAgents.py`, `util.py`, `game.py`, etc.) corresponde
a la adaptación clásica de Berkeley/Stanford CS221 usada en la guía de laboratorio, y se conserva
sin cambios de arquitectura, tal como lo exige el enunciado.

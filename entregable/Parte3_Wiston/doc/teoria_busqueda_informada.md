# Teoría necesaria para entender la Parte 3 (Actividades 10 y 11)

> Documento de estudio, no es el informe formal (ese es `explicacion_parte3.pdf`). Aquí se explica
> el "por qué" detrás de cada pieza de código, para poder defenderla en la sustentación oral sin
> necesidad de memorizar nada.

## 1. Qué es un problema de búsqueda

Todo problema de búsqueda de este taller se representa con seis componentes:

$$P = (S, A, T, s_0, G, C)$$

- **S**: el conjunto de estados posibles.
- **A**: las acciones disponibles en cada estado (aquí siempre `North`, `South`, `East`, `West`).
- **T**: la función de transición (a qué estado se llega al aplicar una acción).
- **s₀**: el estado inicial.
- **G**: la prueba de objetivo (cómo saber si un estado es una meta).
- **C**: el costo de cada acción.

En código, esto se traduce directamente en la interfaz `SearchProblem` de `search.py`:
`getStartState()` es s₀, `isGoalState(state)` es G, `getSuccessors(state)` combina A y T (te da,
para un estado, todos los pares `(sucesor, acción, costo)`), y `getCostOfActions(actions)` usa C.

Lo importante de la Parte 3 es que **S cambia de forma** entre problemas: en
`PositionSearchProblem` (Actividades 2-6) un estado es solo una posición `(x, y)`. En
`FoodSearchProblem` (Actividades 10-11) un estado es un par `(posición, foodGrid)`, donde
`foodGrid` es una matriz booleana con qué alimentos siguen presentes. El algoritmo de búsqueda
(UCS o A*) no cambia en absoluto entre ambos problemas — solo cambia qué representa un "estado", y
eso lo decide `SearchProblem`, no el algoritmo.

## 2. Por qué el espacio de estados de FoodSearchProblem es mucho más grande

Si el laberinto tiene $F$ alimentos, cada uno puede estar en dos condiciones: presente o
consumido. El número de configuraciones posibles del `foodGrid` es, conceptualmente, $2^F$. Con
solo 8 alimentos (`testClassic`) ya hay hasta 256 configuraciones de comida posibles combinadas
con cada posición de Pac-Man; con 55 alimentos (`smallClassic`), $2^{55}$ es un número
astronómico. Esto se confirmó experimentalmente: `uniformCostSearch` sobre `smallClassic` no
terminó en 45 segundos, mientras que sobre `testClassic` (8 alimentos) UCS expande 2598 nodos en
menos de un décimo de segundo. Esta es la razón concreta por la que hace falta diseñar una buena
heurística: sin ella, el algoritmo se vuelve intratable en cuanto crece el número de alimentos.

## 3. Búsqueda de costo uniforme (UCS) y A*: el mismo esqueleto

UCS ordena su frontera (una cola de prioridad) por $g(n)$, el costo acumulado real desde el
estado inicial. A* ordena la misma frontera por $f(n) = g(n) + h(n)$, donde $h(n)$ es una
heurística que estima cuánto falta para llegar a la meta. Si $h(n) = 0$ para todo estado, A* se
reduce exactamente a UCS (confirmado en la Actividad 10: UCS y A*+h=0 dan siempre el mismo costo y
el mismo número de nodos expandidos, tanto en `PositionSearchProblem` como en `FoodSearchProblem`).

Ambos algoritmos, en este proyecto, usan el patrón de **"goal test on pop"**: se comprueba si un
estado es meta justo cuando se extrae de la cola de prioridad (no cuando se genera como sucesor).
Esto es lo que garantiza optimalidad: como la cola siempre entrega primero el estado de menor
prioridad conocida, la primera vez que se extrae un estado meta, es a través del camino más barato
posible que ya se ha descubierto.

## 4. Admisibilidad y consistencia (por qué importan para foodHeuristic)

Una heurística $h(n)$ es **admisible** si nunca sobreestima el costo real restante:

$$0 \le h(n) \le h^*(n)$$

Esto garantiza que A* siga encontrando la solución óptima (nunca descarta injustamente un camino
bueno por creer, equivocadamente, que es peor de lo que realmente es).

Una heurística es **consistente** (más fuerte que admisible) si para cualquier estado $n$ y
cualquier sucesor $n'$ (con costo de transición $c(n,n')$):

$$h(n) \le c(n,n') + h(n')$$

y además $h(\text{meta}) = 0$. La consistencia es justo lo que el docstring original de
`foodHeuristic` pedía explícitamente ("this heuristic must be consistent to ensure correctness"),
a diferencia de `cornersHeuristic` (Actividad 8, Parte 2), donde solo se pide admisibilidad. La
consistencia es importante porque, junto con el patrón "goal test on pop", garantiza que ningún
nodo necesite reabrirse: una vez que A* extrae un estado de la frontera, ya sabe que encontró su
mejor costo posible.

### Por qué la distancia Manhattan es admisible y consistente aquí

Pac-Man se mueve solo en 4 direcciones (nunca en diagonal). La distancia Manhattan entre dos puntos
$n=(x_n,y_n)$ y $g=(x_g,y_g)$ es:

$$d_M(n,g) = |x_n - x_g| + |y_n - y_g|$$

Es admisible porque ignora las paredes: el camino real (que sí tiene que rodearlas) nunca puede ser
más corto que la distancia en línea recta ortogonal que calcula $d_M$. Es consistente porque, para
cualquier paso ortogonal de costo 1, la distancia Manhattan a cualquier punto fijo cambia como
máximo en 1 (la desigualdad triangular aplicada a esta métrica).

## 5. Las dos heurísticas diseñadas para foodHeuristic

**Heurística 1** (`foodHeuristicV1`), la fórmula que sugiere la guía directamente:

$$h(n) = \max_{f \in F} d_M(n, f)$$

La distancia Manhattan al alimento restante más lejano. Es admisible (el costo real de recoger
toda la comida es, como mínimo, el de llegar hasta el más lejano) y consistente (por el mismo
argumento de desigualdad triangular del punto 4, aplicado con cuidado al caso en que el alimento
más lejano es justo el que se acaba de comer — ver la demostración completa en
`explicacion_parte3.pdf`).

**Heurística 2** (`foodHeuristic`, la que realmente usa el agente), una generalización: en vez de
mirar solo la distancia de Pac-Man al alimento más lejano, se considera el **diámetro** (la mayor
distancia Manhattan entre cualquier par de puntos) del conjunto {posición actual} ∪ {alimentos
restantes}:

$$h(n) = \max\Big(\max_{f \in F} d_M(n,f),\ \max_{f_i,f_j \in F} d_M(f_i,f_j)\Big)$$

La intuición: para visitar dos alimentos lejanos entre sí, en algún momento del recorrido Pac-Man
tiene que atravesar al menos esa distancia entre ellos, sin importar dónde esté parado ahora
mismo. Por eso Heurística 2 es siempre al menos tan informativa como Heurística 1 (nunca expande
más nodos), y en la práctica expande bastantes menos: en `testClassic`, Heurística 1 expande 702
nodos y Heurística 2 expande 383, frente a los 2598 de no usar ninguna heurística.

## 6. El caché con `problem.heuristicInfo`: qué se guarda y por qué (y por qué no siempre ayuda)

Como las posiciones de los alimentos nunca cambian durante la búsqueda (solo si siguen presentes o
no), la distancia Manhattan entre cada par de alimentos del layout inicial se puede calcular una
sola vez y reutilizarse en cada llamada a la heurística, en vez de recalcularla cada vez.

El hallazgo honesto de esta actividad es que, midiéndolo, **el caché no mejoró el tiempo** (salió
entre 4% y 7% más lento en dos layouts distintos). La explicación: lo que se cachea es aritmética
de enteros (una resta), y consultar un diccionario de Python con una tupla como llave tiene su
propio costo (construir la tupla, calcular su hash) que, en este caso concreto, es comparable o
mayor al costo de simplemente volver a restar. El caché con `problem.heuristicInfo` sigue siendo la
herramienta correcta que sugiere la guía; su beneficio depende de que lo que se evite recalcular
sea realmente costoso (como una búsqueda BFS completa para una distancia real de laberinto), no
aritmética trivial. Esta es una lección real de ingeniería de software, no un error de
implementación: los nodos expandidos son idénticos en ambas versiones (con y sin caché), porque es
exactamente la misma heurística — lo único que cambia es cómo se calcula cada valor internamente.

## 7. Glosario rápido para la sustentación

- **$g(n)$**: costo acumulado real desde el estado inicial hasta el estado $n$.
- **$h(n)$**: estimación heurística del costo restante desde $n$ hasta la meta.
- **$f(n) = g(n) + h(n)$**: la prioridad que usa A* para decidir qué nodo expandir primero.
- **Nodo expandido**: un estado del cual se generaron sus sucesores (se llamó a `getSuccessors`).
  No es lo mismo que "nodo insertado en la frontera": un mismo estado puede insertarse varias veces
  pero solo se expande la primera vez que resulta ser realmente óptimo llegar a él.
- **Factor de reducción $R = N_{UCS} / N_{A^*}$**: cuántas veces menos nodos expandió A* respecto a
  UCS. En `testClassic`, $R \approx 2598/383 \approx 6.78$ con la Heurística 2.

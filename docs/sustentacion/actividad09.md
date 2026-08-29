# Sustentación — Actividad 9: Experimento comparativo (esquinas)

> Uso interno del grupo. No se entrega al profesor.

## Qué se hizo
Se corrieron UCS, A*+h=0, A*+heurística básica y A*+heurística propuesta sobre `tinyCorners` y se
armó la tabla comparativa que pide la guía, más el factor de reducción R = N_UCS/N_A* = 295/119 =
2.48 (usando la heurística propuesta como referencia).

## Partes críticas del código

- **Cada estrategia corre sobre una instancia NUEVA de `CornersProblem`** (`_nuevo_problema(...)`
  llamado una vez por método) — necesario porque `problem._expanded` es un contador que vive
  dentro de la instancia; si se reutilizara la misma instancia para las cuatro corridas, los
  conteos se acumularían entre métodos y la tabla saldría mal.
- **El costo óptimo de referencia sale de la corrida de UCS**, no de un número fijo en el código —
  así, si alguien cambiara de layout, el script se sigue verificando a sí mismo en vez de comparar
  contra un número hardcodeado que podría quedar desactualizado.
- **Bug encontrado y corregido durante el desarrollo:** en la primera versión del script, la fila
  de UCS se guardaba comparando su propio costo contra `costo_optimo_referencia=None`, lo que hacía
  que la columna "óptimo" saliera "no" para UCS (comparación `22 == None` es falsa) — un error
  claramente absurdo, porque UCS es óptimo por definición. Se corrigió guardando la fila de UCS por
  separado, siempre con `optimo="si"`, sin pasar por la comparación genérica. Vale la pena
  mencionarlo si preguntan: es un buen ejemplo de por qué hay que revisar el CSV generado, no solo
  confiar en que el código "debería" estar bien.

## ¿Qué pasa si...?

- **¿Qué pasa si UCS y A*+h=0 dieran números de nodos expandidos distintos?**
  Sería señal de un bug: matemáticamente, A* con `h(n)=0` para todo n es exactamente UCS (el orden
  de expansión de la cola de prioridad depende únicamente de `g(n)`, igual en ambos). Aquí
  coinciden exactamente (295 en los dos), como se espera.
- **¿Qué pasa si se usara un layout más grande que tinyCorners para este experimento?**
  El patrón se mantendría (h=0 = UCS; básica y propuesta reducen expansiones sin perder
  optimalidad), pero R probablemente sería mayor: entre más grande el espacio de búsqueda, más
  margen tiene una buena heurística para evitar exploración innecesaria. No se probó con
  `mediumCorners` por el hallazgo de la Actividad 7 (layout sellado).

## Preguntas trampa esperadas del profesor

1. **"¿Por qué calcularon R usando la heurística propuesta y no la básica?"**
   Porque R busca mostrar la reducción lograda por la MEJOR heurística disponible; se menciona
   también el R de la básica (2.01) para comparar, pero el número principal usa la más informada,
   que es la que efectivamente usa `AStarCornersAgent`.
2. **"¿El factor R de 2.48 es bueno o esperable para este tipo de problema?"**
   Es razonable para un layout tan pequeño como `tinyCorners` (namespace de estados chico): en
   problemas más grandes, con más margen para que la heurística "guíe" la búsqueda, R tiende a
   crecer. Lo importante no es el valor absoluto sino que R > 1 en ambas heurísticas, confirmando
   que sí ayudan.
3. **"¿Cómo verificaron que ninguna de las cuatro estrategias perdió optimalidad?"**
   El script compara el costo de cada estrategia contra el costo de UCS (que es óptimo por
   definición) y usa un `assert` que detiene la ejecución si alguna no coincide — no es solo una
   inspección visual de la tabla, es una verificación automática en cada corrida.

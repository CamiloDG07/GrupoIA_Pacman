"""
_resultados.py
---------------
Pequeno helper para que todos los scripts de experimentos/ escriban en el
mismo resultados/resultados.csv sin duplicar filas cuando un experimento se
vuelve a correr (por ejemplo, tras ajustar una heuristica).

Columnas: actividad, metodo_heuristica, layout, costo, longitud_camino,
nodos_expandidos, tiempo_seg, optimo
"""
import csv
import os

from _bootstrap import resultados_csv_path

FIELDS = [
    "actividad",
    "metodo_heuristica",
    "layout",
    "costo",
    "longitud_camino",
    "nodos_expandidos",
    "tiempo_seg",
    "optimo",
]


def guardar_fila(fila: dict):
    """Inserta o reemplaza (actividad, metodo_heuristica, layout) en el CSV."""
    path = resultados_csv_path()
    filas = []
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))

    clave = (fila["actividad"], fila["metodo_heuristica"], fila["layout"])
    filas = [
        f for f in filas
        if (f.get("actividad"), f.get("metodo_heuristica"), f.get("layout")) != clave
    ]
    filas.append(fila)

    # Orden estable: por actividad y luego por metodo, para que el CSV sea
    # legible directamente (y facil de pegar en la tabla del informe).
    filas.sort(key=lambda f: (f.get("actividad", ""), f.get("metodo_heuristica", "")))

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(filas)

"""
_bootstrap.py
-------------
Utilidad compartida por todos los scripts de experimentos/.

El motor de Pac-Man (layout.py) busca la carpeta "layouts/" relativa al
directorio de trabajo actual, y search.py / searchAgents.py se importan
como módulos sueltos (no como paquete). Por eso cada script de actividad
llama primero a bootstrap() para:

  1) agregar pacman/ al sys.path (para poder hacer `import search`,
     `import searchAgents`, `import pacman`, `import layout`);
  2) ubicarse (chdir) dentro de pacman/ para que los .lay se encuentren.

Así el código base del profesor (pacman/) permanece intacto: los scripts
de experimentos solo lo consumen desde afuera.
"""
import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PACMAN_DIR = os.path.normpath(os.path.join(_THIS_DIR, "..", "pacman"))
REPO_ROOT = os.path.normpath(os.path.join(_THIS_DIR, ".."))


def bootstrap():
    if PACMAN_DIR not in sys.path:
        sys.path.insert(0, PACMAN_DIR)
    os.chdir(PACMAN_DIR)
    return PACMAN_DIR


def resultados_csv_path():
    return os.path.join(REPO_ROOT, "resultados", "resultados.csv")

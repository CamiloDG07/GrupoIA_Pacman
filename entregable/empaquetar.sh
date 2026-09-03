#!/usr/bin/env bash
# Arma GrupoXX_Pacman_AStar.zip exactamente con la estructura que pide el
# enunciado (pagina 16 de la guia):
#
#   GrupoXX_Pacman_AStar.zip
#   |-- search.py
#   |-- searchAgents.py
#   |-- resultados.csv
#   '-- informe.pdf
#
# Uso:
#   ./entregable/empaquetar.sh GrupoXX
# (reemplace GrupoXX por el numero de grupo real, ej. Grupo03)

set -euo pipefail
cd "$(dirname "$0")/.."

GRUPO="${1:-GrupoXX}"
STAGE="entregable/${GRUPO}_Pacman_AStar"
ZIP="entregable/${GRUPO}_Pacman_AStar.zip"

rm -rf "$STAGE" "$ZIP"
mkdir -p "$STAGE"

cp pacman/search.py "$STAGE/"
cp pacman/searchAgents.py "$STAGE/"
cp resultados/resultados.csv "$STAGE/"

if [ -f informe.pdf ]; then
    cp informe.pdf "$STAGE/"
else
    echo "AVISO: no existe informe.pdf en la raiz del repositorio."
    exit 1
fi


# Los 4 archivos van SUELTOS en la raiz del zip (no dentro de una subcarpeta):
# el enunciado los lista como GrupoXX_Pacman_AStar.zip/search.py, no
# GrupoXX_Pacman_AStar.zip/GrupoXX_Pacman_AStar/search.py.
(cd "$STAGE" && zip -r "../$(basename "$ZIP")" . -x '*.DS_Store')
rm -rf "$STAGE"

echo "Listo: $ZIP"

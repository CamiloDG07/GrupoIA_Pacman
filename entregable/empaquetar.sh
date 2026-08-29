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

if [ -f docs/latex/informe.pdf ]; then
    cp docs/latex/informe.pdf "$STAGE/"
else
    echo "AVISO: no existe docs/latex/informe.pdf. Compile primero:"
    echo "  cd docs/latex && pdflatex informe.tex && pdflatex informe.tex"
    exit 1
fi

(cd entregable && zip -r "$(basename "$ZIP")" "$(basename "$STAGE")" -x '*.DS_Store')
rm -rf "$STAGE"

echo "Listo: $ZIP"

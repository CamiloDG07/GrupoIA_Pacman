"""
Genera imagenes "placeholder" para las capturas de pantalla que Camilo debe
tomar en su VS Code local. Cada imagen indica claramente: archivo, rango de
lineas, funcion y que se debe capturar. Al reemplazar el .png (mismo nombre)
por una captura real de VS Code, el informe.tex no necesita ningun otro
cambio -- el \\includegraphics ya apunta al mismo archivo.

Uso: python3 _generar_placeholders.py
"""
from PIL import Image, ImageDraw, ImageFont

FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1500
PAD = 36
LINE_H = 30
HEADER_H = 110

BG = (30, 31, 38)          # fondo estilo VS Code oscuro
HEADER_BG = (20, 99, 165)  # azul de aviso
TEXT_CODE = (214, 214, 214)
TEXT_KEYWORD = (86, 156, 214)
TEXT_COMMENT = (106, 153, 85)
BORDER = (220, 60, 60)

def resaltar(linea):
    """Colorea de forma muy simple palabras clave de Python."""
    keywords = ["def", "if", "for", "in", "not", "return", "while", "and", "or", "None"]
    partes = []
    palabra = ""
    for ch in linea:
        if ch.isalnum() or ch == "_":
            palabra += ch
        else:
            if palabra:
                partes.append((palabra, TEXT_KEYWORD if palabra in keywords else TEXT_CODE))
                palabra = ""
            partes.append((ch, TEXT_CODE))
    if palabra:
        partes.append((palabra, TEXT_KEYWORD if palabra in keywords else TEXT_CODE))
    return partes


def generar(nombre_archivo, archivo, lineas_rango, funcion, codigo_lineas, nota=""):
    n = len(codigo_lineas)
    h = HEADER_H + PAD + n * LINE_H + PAD + (LINE_H if nota else 0)
    img = Image.new("RGB", (W, h), BG)
    draw = ImageDraw.Draw(img)

    font_header_title = ImageFont.truetype(FONT_SANS_BOLD, 26)
    font_header_sub = ImageFont.truetype(FONT_MONO, 20)
    font_code = ImageFont.truetype(FONT_MONO, 21)
    font_nota = ImageFont.truetype(FONT_MONO, 18)

    # Cabecera de aviso
    draw.rectangle([0, 0, W, HEADER_H], fill=HEADER_BG)
    draw.text((PAD, 14), "PANTALLAZO PENDIENTE — reemplazar por captura real de VS Code",
              font=font_header_title, fill=(255, 255, 255))
    draw.text((PAD, 54), f"Archivo: {archivo}   |   Lineas: {lineas_rango}   |   Funcion: {funcion}",
              font=font_header_sub, fill=(225, 235, 250))

    # Cuerpo de código (referencia, para ubicar el bloque exacto)
    y = HEADER_H + PAD
    for linea in codigo_lineas:
        x = PAD
        for texto, color in resaltar(linea):
            draw.text((x, y), texto, font=font_code, fill=color)
            x += draw.textlength(texto, font=font_code)
        y += LINE_H

    if nota:
        draw.text((PAD, y + 6), nota, font=font_nota, fill=(180, 180, 100))

    # Borde punteado (marca visual de "placeholder")
    for x in range(0, W, 18):
        draw.line([(x, 2), (x + 9, 2)], fill=BORDER, width=4)
        draw.line([(x, h - 3), (x + 9, h - 3)], fill=BORDER, width=4)
    for yy in range(0, h, 18):
        draw.line([(2, yy), (2, yy + 9)], fill=BORDER, width=4)
        draw.line([(W - 3, yy), (W - 3, yy + 9)], fill=BORDER, width=4)

    img.save(nombre_archivo)
    print("Generado:", nombre_archivo, img.size)


SLOTS = [
    dict(
        nombre_archivo="actividad02_ucs.png",
        archivo="pacman/search.py", lineas_rango="111-142", funcion="uniformCostSearch",
        codigo_lineas=[
            "def uniformCostSearch(problem):",
            "  frontier = util.PriorityQueue()",
            "  startState = problem.getStartState()",
            "  contador = 0",
            "  frontier.push((contador, startState, [], 0), 0)",
            "  bestCost = {startState: 0}",
            "  while not frontier.isEmpty():",
            "    _, state, actions, cost = frontier.pop()",
            "    if cost > bestCost.get(state, float('inf')):",
            "      continue",
            "    if problem.isGoalState(state):",
            "      return actions",
            "    for successor, action, stepCost in problem.getSuccessors(state):",
            "      newCost = cost + stepCost",
            "      if newCost < bestCost.get(successor, float('inf')):",
            "        bestCost[successor] = newCost",
            "        contador += 1",
            "        frontier.push((contador, successor, actions+[action], newCost), newCost)",
            "  return []",
        ],
        nota="Capturar TODO el bloque, incluido el 'contador' (tie-breaker) -- es el hallazgo clave de la Actividad 2/3.",
    ),
    dict(
        nombre_archivo="actividad03_astar.png",
        archivo="pacman/search.py", lineas_rango="178-211", funcion="aStarSearch",
        codigo_lineas=[
            "def aStarSearch(problem, heuristic=nullHeuristic):",
            "  frontier = util.PriorityQueue()",
            "  startState = problem.getStartState()",
            "  contador = 0",
            "  startPriority = 0 + heuristic(startState, problem)  # f = g + h",
            "  frontier.push((contador, startState, [], 0), startPriority)",
            "  bestCost = {startState: 0}",
            "  while not frontier.isEmpty():",
            "    _, state, actions, cost = frontier.pop()",
            "    if cost > bestCost.get(state, float('inf')):",
            "      continue",
            "    if problem.isGoalState(state):",
            "      return actions",
            "    for successor, action, stepCost in problem.getSuccessors(state):",
            "      newCost = cost + stepCost",
            "      if newCost < bestCost.get(successor, float('inf')):",
            "        bestCost[successor] = newCost",
            "        contador += 1",
            "        priority = newCost + heuristic(successor, problem)  # f(n)=g(n)+h(n)",
            "        frontier.push((contador, successor, actions+[action], newCost), priority)",
            "  return []",
        ],
        nota="Comparar visualmente con la captura de UCS: la UNICA diferencia real es la linea de 'priority'.",
    ),
    dict(
        nombre_archivo="actividad05_manhattan.png",
        archivo="pacman/searchAgents.py", lineas_rango="236-240", funcion="manhattanHeuristic",
        codigo_lineas=[
            "def manhattanHeuristic(position, problem, info={}):",
            "  xy1 = position",
            "  xy2 = problem.goal",
            "  return abs(xy1[0]-xy2[0]) + abs(xy1[1]-xy2[1])",
        ],
    ),
    dict(
        nombre_archivo="actividad06_euclidiana.png",
        archivo="pacman/searchAgents.py", lineas_rango="242-246", funcion="euclideanHeuristic",
        codigo_lineas=[
            "def euclideanHeuristic(position, problem, info={}):",
            "  xy1 = position",
            "  xy2 = problem.goal",
            "  return ((xy1[0]-xy2[0])**2 + (xy1[1]-xy2[1])**2) ** 0.5",
        ],
    ),
    dict(
        nombre_archivo="actividad07_corners.png",
        archivo="pacman/searchAgents.py", lineas_rango="273-351",
        funcion="getStartState / isGoalState / getSuccessors (CornersProblem)",
        codigo_lineas=[
            "def getStartState(self):",
            "  esquinasVisitadas = (False, False, False, False)",
            "  return (self.startingPosition, esquinasVisitadas)",
            "",
            "def isGoalState(self, state):",
            "  _, esquinasVisitadas = state",
            "  return all(esquinasVisitadas)",
            "",
            "def getSuccessors(self, state):",
            "  position, visited = state",
            "  ... # por cada direccion legal:",
            "  nextPosition = (nextx, nexty)",
            "  nextVisited = visited",
            "  if nextPosition in self.corners:",
            "    idx = self.corners.index(nextPosition)",
            "    if not visited[idx]:",
            "      nextVisited = visited[:idx] + (True,) + visited[idx+1:]",
            "  nextState = (nextPosition, nextVisited)",
        ],
        nota="Capturar las 3 funciones completas -- el punto clave es el par (posicion, esquinas_visitadas) como estado.",
    ),
    dict(
        nombre_archivo="actividad08_heuristica_basica.png",
        archivo="pacman/searchAgents.py", lineas_rango="367-396", funcion="cornersHeuristicBasica",
        codigo_lineas=[
            "def cornersHeuristicBasica(state, problem):",
            "  position, visited = state",
            "  corners = problem.corners",
            "  pendientes = [c for c, v in zip(corners, visited) if not v]",
            "  if not pendientes:",
            "    return 0",
            "  return max(abs(position[0]-c[0]) + abs(position[1]-c[1])",
            "             for c in pendientes)",
        ],
    ),
    dict(
        nombre_archivo="actividad08_heuristica_propuesta.png",
        archivo="pacman/searchAgents.py", lineas_rango="399-452", funcion="cornersHeuristic",
        codigo_lineas=[
            "def cornersHeuristic(state, problem):",
            "  position, visited = state",
            "  corners = problem.corners",
            "  pendientes = [c for c, v in zip(corners, visited) if not v]",
            "  if not pendientes:",
            "    return 0",
            "  puntos = [position] + pendientes",
            "  maxDist = 0",
            "  for i in range(len(puntos)):",
            "    for j in range(i+1, len(puntos)):",
            "      d = abs(puntos[i][0]-puntos[j][0]) + abs(puntos[i][1]-puntos[j][1])",
            "      if d > maxDist:",
            "        maxDist = d",
            "  return maxDist",
        ],
        nota="Comparar con la basica: aqui se recorren TODOS los pares de {posicion}+pendientes, no solo posicion->esquina.",
    ),
    dict(
        nombre_archivo="actividad10_food_isgoal.png",
        archivo="pacman/searchAgents.py", lineas_rango="460-480",
        funcion="FoodSearchProblem.__init__ / isGoalState",
        codigo_lineas=[
            "class FoodSearchProblem:",
            "  def __init__(self, startingGameState):",
            "    self.start = (startingGameState.getPacmanPosition(),",
            "                  startingGameState.getFood())",
            "    ...",
            "  def isGoalState(self, state):",
            "    return state[1].count() == 0",
        ],
        nota="Lo clave a resaltar: el estado es (posicion, foodGrid) -- no solo la posicion.",
    ),
    dict(
        nombre_archivo="actividad11_heuristica1.png",
        archivo="pacman/searchAgents.py", lineas_rango="516-540", funcion="foodHeuristicV1",
        codigo_lineas=[
            "def foodHeuristicV1(state, problem):",
            "  position, foodGrid = state",
            "  foodList = foodGrid.asList()",
            "  if not foodList:",
            "    return 0",
            "  return max(abs(position[0]-f[0]) + abs(position[1]-f[1])",
            "             for f in foodList)",
        ],
    ),
    dict(
        nombre_archivo="actividad11_heuristica2.png",
        archivo="pacman/searchAgents.py", lineas_rango="543-608", funcion="foodHeuristic (con cache)",
        codigo_lineas=[
            "def foodHeuristic(state, problem):",
            "  position, foodGrid = state",
            "  foodList = foodGrid.asList()",
            "  if not foodList: return 0",
            "  if 'foodPairDistances' not in problem.heuristicInfo:",
            "    allFood = problem.start[1].asList()",
            "    distancias = {}",
            "    for i in range(len(allFood)):",
            "      for j in range(i+1, len(allFood)):",
            "        d = abs(allFood[i][0]-allFood[j][0]) + abs(allFood[i][1]-allFood[j][1])",
            "        distancias[(allFood[i],allFood[j])] = d",
            "        distancias[(allFood[j],allFood[i])] = d",
            "    problem.heuristicInfo['foodPairDistances'] = distancias",
            "  distanciasComida = problem.heuristicInfo['foodPairDistances']",
            "  maxDist = 0  # ... max entre posicion->comida y comida<->comida",
            "  return maxDist",
        ],
        nota="Resaltar el bloque 'if foodPairDistances not in heuristicInfo' -- es el cache, tema de la Actividad 11.",
    ),
]

if __name__ == "__main__":
    for slot in SLOTS:
        generar(**slot)

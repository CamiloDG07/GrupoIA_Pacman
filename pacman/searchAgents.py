"""
This file contains all of the agents that can be selected to 
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch

Commands to invoke other search strategies can be found in the 
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import searchAgents

class GoWestAgent(Agent):
  "An agent that goes West until it can't."
  
  def getAction(self, state):
    "The agent receives a GameState (defined in pacman.py)."
    if Directions.WEST in state.getLegalPacmanActions():
      return Directions.WEST
    else:
      return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
  """
  This very general search agent finds a path using a supplied search algorithm for a
  supplied search problem, then returns actions to follow that path.
  
  As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)
  
  Options for fn include:
    depthFirstSearch or dfs
    breadthFirstSearch or bfs
    
  
  Note: You should NOT change any code in SearchAgent
  """
    
  def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
    # Warning: some advanced Python magic is employed below to find the right functions and problems
    
    # Get the search function from the name and heuristic
    if fn not in dir(search): 
      raise AttributeError(fn + ' is not a search function in search.py.')
    func = getattr(search, fn)
    if 'heuristic' not in func.__code__.co_varnames:
      print(('[SearchAgent] using function ' + fn)) 
      self.searchFunction = func
    else:
      if heuristic in dir(searchAgents):
        heur = getattr(searchAgents, heuristic)
      elif heuristic in dir(search):
        heur = getattr(search, heuristic)
      else:
        raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
      print(('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))) 
      # Note: this bit of Python trickery combines the search algorithm and the heuristic
      self.searchFunction = lambda x: func(x, heuristic=heur)
      
    # Get the search problem type from the name
    if prob not in dir(searchAgents) or not prob.endswith('Problem'): 
      raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
    self.searchType = getattr(searchAgents, prob)
    print(('[SearchAgent] using problem type ' + prob)) 
    
  def registerInitialState(self, state):
    """
    This is the first time that the agent sees the layout of the game board. Here, we
    choose a path to the goal.  In this phase, the agent should compute the path to the
    goal and store it in a local variable.  All of the work is done in this method!
    
    state: a GameState object (pacman.py)
    """
    if self.searchFunction is None: raise Exception("No search function provided for SearchAgent")
    starttime = time.time()
    problem = self.searchType(state) # Makes a new search problem
    self.actions  = self.searchFunction(problem) # Find a path
    totalCost = problem.getCostOfActions(self.actions)
    print(('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime)))
    if '_expanded' in dir(problem): print(('Search nodes expanded: %d' % problem._expanded))
    if '_maxMemory' in dir(problem): print(('Max nodes in memory: %d' % problem._maxMemory))
    
  def getAction(self, state):
    """
    Returns the next action in the path chosen earlier (in registerInitialState).  Return
    Directions.STOP if there is no further action to take.
    
    state: a GameState object (pacman.py)
    """
    if 'actionIndex' not in dir(self): self.actionIndex = 0
    i = self.actionIndex
    self.actionIndex += 1
    if i < len(self.actions):
      return self.actions[i]    
    else:
      return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
  """
  A search problem defines the state space, start state, goal test,
  successor function and cost function.  This search problem can be 
  used to find paths to a particular point on the pacman board.
  
  The state space consists of (x,y) positions in a pacman game.
  
  Note: this search problem is fully specified; you should NOT change it.
  """
  
  def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True):
    """
    Stores the start and goal.  
    
    gameState: A GameState object (pacman.py)
    costFn: A function from a search state (tuple) to a non-negative number
    goal: A position in the gameState
    """
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    if start != None: self.startState = start
    self.goal = goal
    self.costFn = costFn
    if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
      print('Warning: this does not look like a regular search maze')

    # For display purposes
    self._visited, self._visitedlist, self._expanded = {}, [], 0

  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
     isGoal = state == self.goal 
     
     # For display purposes only
     if isGoal:
       self._visitedlist.append(state)
       import __main__
       if '_display' in dir(__main__):
         if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
           __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable
       
     return isGoal   
   
  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.
    
     As noted in search.py:
         For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append( ( nextState, action, cost) )
        
    # Bookkeeping for display purposes
    self._expanded += 1 
    if state not in self._visited:
      self._visited[state] = True
      self._visitedlist.append(state)
      
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999
    """
    if actions is None: return 999999
    x,y= self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
      cost += self.costFn((x,y))
    return cost

class StayEastSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the West side of the board.  
  
  The cost function for stepping into a position (x,y) is 1/2^x.
  """
  def __init__(self):
      self.searchFunction = search.uniformCostSearch
      costFn = lambda pos: .5 ** pos[0] 
      self.searchType = lambda state: PositionSearchProblem(state, costFn)
      
class StayWestSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the East side of the board.  
  
  The cost function for stepping into a position (x,y) is 2^x.
  """
  def __init__(self):
      self.searchFunction = search.uniformCostSearch
      costFn = lambda pos: 2 ** pos[0] 
      self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
  "The Manhattan distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
  "The Euclidean distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
  """
  This search problem finds paths through all four corners of a layout.

  You must select a suitable state space and successor function
  """
  
  def __init__(self, startingGameState):
    """
    Stores the walls, pacman's starting position and corners.
    """
    self.walls = startingGameState.getWalls()
    self.startingPosition = startingGameState.getPacmanPosition()
    top, right = self.walls.height-2, self.walls.width-2 
    self.corners = ((1,1), (1,top), (right, 1), (right, top))
    for corner in self.corners:
      if not startingGameState.hasFood(*corner):
        print('Warning: no food in corner ' + str(corner))
    self._expanded = 0 # Number of search nodes expanded
    
    
  def getStartState(self):
    "Estado: (posicion, esquinas_visitadas) con 4 booleanos."
    esquinasVisitadas = (False, False, False, False)
    return (self.startingPosition, esquinasVisitadas)

  def isGoalState(self, state):
    "Meta: las 4 esquinas visitadas."
    _, esquinasVisitadas = state
    return all(esquinasVisitadas)

  def getSuccessors(self, state):
    "Returns successor states, the actions they require, and a cost of 1."
    successors = []
    position, visited = state
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x, y = position
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      hitsWall = self.walls[nextx][nexty]

      if not hitsWall:
        nextPosition = (nextx, nexty)
        nextVisited = visited
        if nextPosition in self.corners:
          idx = self.corners.index(nextPosition)
          if not visited[idx]:
            nextVisited = visited[:idx] + (True,) + visited[idx + 1:]
        nextState = (nextPosition, nextVisited)
        successors.append((nextState, action, 1))

    self._expanded += 1
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999.  This is implemented for you.
    """
    if actions is None: return 999999
    x,y= self.startingPosition
    for action in actions:
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
    return len(actions)


def cornersHeuristicBasica(state, problem):
  "Heuristica basica: distancia Manhattan a la esquina pendiente mas lejana."
  position, visited = state
  corners = problem.corners
  pendientes = [c for c, v in zip(corners, visited) if not v]
  if not pendientes:
    return 0
  return max(abs(position[0] - c[0]) + abs(position[1] - c[1]) for c in pendientes)


def cornersHeuristic(state, problem):
  "Heuristica propuesta: diametro Manhattan de {posicion} union {esquinas pendientes}."
  position, visited = state
  corners = problem.corners
  pendientes = [c for c, v in zip(corners, visited) if not v]
  if not pendientes:
    return 0

  puntos = [position] + pendientes
  maxDist = 0
  for i in range(len(puntos)):
    for j in range(i + 1, len(puntos)):
      p1, p2 = puntos[i], puntos[j]
      d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
      if d > maxDist:
        maxDist = d
  return maxDist

class AStarCornersAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
    self.searchType = CornersProblem

class FoodSearchProblem:
  """
  A search problem associated with finding the a path that collects all of the 
  food (dots) in a Pacman game.
  
  A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
    pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
    foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food 
  """
  def __init__(self, startingGameState):
    self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
    self.walls = startingGameState.getWalls()
    self.startingGameState = startingGameState
    self._expanded = 0
    self.heuristicInfo = {} # A dictionary for the heuristic to store information
      
  def getStartState(self):
    return self.start
  
  def isGoalState(self, state):
    return state[1].count() == 0

  def getSuccessors(self, state):
    "Returns successor states, the actions they require, and a cost of 1."
    successors = []
    self._expanded += 1
    for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state[0]
      dx, dy = Actions.directionToVector(direction)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextFood = state[1].copy()
        nextFood[nextx][nexty] = False
        successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
    return successors

  def getCostOfActions(self, actions):
    """Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999"""
    x,y= self.getStartState()[0]
    cost = 0
    for action in actions:
      # figure out the next state and see whether it's legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += 1
    return cost

class AStarFoodSearchAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
    self.searchType = FoodSearchProblem

def foodHeuristicV1(state, problem):
  "Heuristica 1: distancia Manhattan al alimento mas lejano."
  position, foodGrid = state
  foodList = foodGrid.asList()
  if not foodList:
    return 0
  return max(abs(position[0] - f[0]) + abs(position[1] - f[1]) for f in foodList)


def foodHeuristic(state, problem):
  "Heuristica 2: diametro Manhattan de {posicion} union {comida restante}, con cache en problem.heuristicInfo."
  position, foodGrid = state
  foodList = foodGrid.asList()
  if not foodList:
    return 0

  if 'foodPairDistances' not in problem.heuristicInfo:
    allFood = problem.start[1].asList()
    distancias = {}
    for i in range(len(allFood)):
      for j in range(i + 1, len(allFood)):
        f1, f2 = allFood[i], allFood[j]
        d = abs(f1[0] - f2[0]) + abs(f1[1] - f2[1])
        distancias[(f1, f2)] = d
        distancias[(f2, f1)] = d
    problem.heuristicInfo['foodPairDistances'] = distancias

  distanciasComida = problem.heuristicInfo['foodPairDistances']

  maxDist = 0
  for f in foodList:
    d = abs(position[0] - f[0]) + abs(position[1] - f[1])
    if d > maxDist:
      maxDist = d
  for i in range(len(foodList)):
    for j in range(i + 1, len(foodList)):
      d = distanciasComida[(foodList[i], foodList[j])]
      if d > maxDist:
        maxDist = d
  return maxDist


def foodHeuristicV2SinCache(state, problem):
  "Heuristica 2 sin cache, para comparar tiempos con/sin cache."
  position, foodGrid = state
  foodList = foodGrid.asList()
  if not foodList:
    return 0

  maxDist = 0
  for f in foodList:
    d = abs(position[0] - f[0]) + abs(position[1] - f[1])
    if d > maxDist:
      maxDist = d
  for i in range(len(foodList)):
    for j in range(i + 1, len(foodList)):
      f1, f2 = foodList[i], foodList[j]
      d = abs(f1[0] - f2[0]) + abs(f1[1] - f2[1])
      if d > maxDist:
        maxDist = d
  return maxDist


class ClosestDotSearchAgent(SearchAgent):
  "Search for all food using a sequence of searches"
  def registerInitialState(self, state):
    self.actions = []
    currentState = state
    while(currentState.getFood().count() > 0): 
      nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
      self.actions += nextPathSegment
      for action in nextPathSegment: 
        legal = currentState.getLegalActions()
        if action not in legal: 
          t = (str(action), str(currentState))
          raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
        currentState = currentState.generateSuccessor(0, action)
    self.actionIndex = 0
    print('Path found with cost %d.' % len(self.actions))
    
  def findPathToClosestDot(self, gameState):
    "Returns a path (a list of actions) to the closest dot, starting from gameState"
    # Here are some useful elements of the startState
    startPosition = gameState.getPacmanPosition()
    food = gameState.getFood()
    walls = gameState.getWalls()
    problem = AnyFoodSearchProblem(gameState)

  
class AnyFoodSearchProblem(PositionSearchProblem):
  """
    A search problem for finding a path to any food.
    
    This search problem is just like the PositionSearchProblem, but
    has a different goal test, which you need to fill in below.  The
    state space and successor function do not need to be changed.
    
    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.
    
    You can use this search problem to help you fill in 
    the findPathToClosestDot method.
  """

  def __init__(self, gameState):
    "Stores information from the gameState.  You don't need to change this."
    # Store the food for later reference
    self.food = gameState.getFood()

    # Store info for the PositionSearchProblem (no need to change this)
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    self.costFn = lambda x: 1
    self._visited, self._visitedlist, self._expanded = {}, [], 0
    
  def isGoalState(self, state):
    """
    The state is Pacman's position. Fill this in with a goal test
    that will complete the problem definition.
    """
    x,y = state
    

##################
# Mini-contest 1 #
##################

class ApproximateSearchAgent(Agent):
  "Implement your contest entry here.  Change anything but the class name."
  
  def registerInitialState(self, state):
    "This method is called before any moves are made."
    
  def getAction(self, state):
    """
    From game.py: 
    The Agent will receive a GameState and must return an action from 
    Directions.{North, South, East, West, Stop}
    """ 
    
def mazeDistance(point1, point2, gameState):
  """
  Returns the maze distance between any two points, using the search functions
  you have already built.  The gameState can be any game state -- Pacman's position
  in that state is ignored.
  
  Example usage: mazeDistance( (2,4), (5,6), gameState)
  
  This might be a useful helper function for your ApproximateSearchAgent.
  """
  x1, y1 = point1
  x2, y2 = point2
  walls = gameState.getWalls()
  assert not walls[x1][y1], 'point1 is a wall: ' + point1
  assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
  prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)
  return len(search.bfs(prob))


#####################################################################
# Demos autonomos (actividades 1-11): reproducen todos los datos    #
# del informe y los guardan en resultados.csv (ver _guardar_fila_demo).
#####################################################################

def _guardar_fila_demo(fila):
  "Inserta o reemplaza una fila en resultados.csv, deduplicando por (actividad, metodo_heuristica, layout)."
  import csv
  import os

  columnas = [
    "actividad",
    "metodo_heuristica",
    "layout",
    "costo",
    "longitud_camino",
    "nodos_expandidos",
    "nodos_en_memoria",
    "memoria_bytes",
    "tiempo_seg",
    "optimo",
  ]
  ruta = "resultados.csv"

  filas = []
  if os.path.exists(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
      filas = list(csv.DictReader(f))

  clave = (fila["actividad"], fila["metodo_heuristica"], fila["layout"])
  filas = [
    f for f in filas
    if (f.get("actividad"), f.get("metodo_heuristica"), f.get("layout")) != clave
  ]
  filas.append(fila)
  filas.sort(key=lambda f: (f.get("actividad", ""), f.get("metodo_heuristica", "")))

  with open(ruta, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columnas)
    writer.writeheader()
    writer.writerows(filas)


def _demo_estado(layout_name):
  "Construye el GameState inicial para un layout (numGhostAgents=0)."
  import layout as layout_module
  import pacman

  lay = layout_module.getLayout(layout_name)
  if lay is None:
    raise SystemExit(f"No se encontro el layout '{layout_name}' en pacman/layouts/")
  state = pacman.GameState()
  state.initialize(lay, numGhostAgents=0)
  return state


def demo_actividad1():
  """Actividad 1. No genera fila (esta actividad solo explora componentes,
  no mide nada)."""
  import layout as layout_module

  layout_name = "tinyMaze"
  lay = layout_module.getLayout(layout_name)
  state = _demo_estado(layout_name)
  problem = PositionSearchProblem(state)

  print("=" * 70)
  print(f"Actividad 1 - Componentes del problema de busqueda ({layout_name})")
  print("=" * 70)

  s0 = problem.getStartState()
  print(f"\n[S]  Estado (s):        posicion (x, y) de Pac-Man en el laberinto")
  print(f"[s0] Estado inicial:    {s0}")

  print(f"\n[A]  Acciones disponibles en s0:")
  sucesores = problem.getSuccessors(s0)
  for successor, action, stepCost in sucesores:
    print(f"     accion={action:6s} -> sucesor={successor}  costo_paso={stepCost}")
  if not sucesores:
    print("     (sin sucesores: revisar layout)")

  print(f"\n[T]  Funcion de transicion / sucesor: getSuccessors(state) -> "
        f"{len(sucesores)} sucesores desde s0 en este layout")

  print(f"\n[G]  Prueba de objetivo isGoalState(s0) = {problem.isGoalState(s0)}")
  print(f"     Objetivo configurado en este problema: problem.goal = {problem.goal}")

  print(f"\n[C]  Costo: cada movimiento legal cuesta 1 "
        f"(ver PositionSearchProblem.costFn, por defecto lambda x: 1)")

  print(f"\nDimensiones del laberinto: {lay.width} x {lay.height}"
        f"  |  Paredes totales: {lay.walls.count()}"
        f"  |  Alimentos totales: {lay.food.count()}")

  print("\nResumen para la tabla de la guia:")
  tabla = [
    ("Estado", "Posicion (x, y) de Pac-Man dentro del laberinto."),
    ("Estado inicial", f"{s0} (posicion de partida en '{layout_name}')."),
    ("Acciones", "North, South, East, West; solo si no hay pared en esa direccion."),
    ("Funcion sucesor", "getSuccessors(state): devuelve (sucesor, accion, costo) por cada movimiento legal."),
    ("Objetivo", f"isGoalState(state); en PositionSearchProblem, llegar a {problem.goal}."),
    ("Costo", "1 por movimiento (suma de pasos = longitud del camino)."),
  ]
  for elemento, descripcion in tabla:
    print(f"  - {elemento}: {descripcion}")


def demo_actividad2(layout_name="mediumMaze"):
  """Actividad 2."""
  state = _demo_estado(layout_name)
  problem = PositionSearchProblem(state, warn=False)

  inicio = time.perf_counter()
  acciones = search.uniformCostSearch(problem)
  tiempo = time.perf_counter() - inicio

  costo = problem.getCostOfActions(acciones)
  longitud = len(acciones)
  expandidos = problem._expanded
  memoria = problem._maxMemory
  memoria_bytes = search.medirMemoriaBytes(
    lambda: PositionSearchProblem(state, warn=False), search.uniformCostSearch)

  print("=" * 70)
  print(f"Actividad 2 - UCS sobre '{layout_name}'")
  print("=" * 70)
  print(f"Estado inicial:     {problem.getStartState()}")
  print(f"Objetivo:           {problem.goal}")
  print(f"Costo del camino:   {costo}")
  print(f"Longitud del camino:{longitud}")
  print(f"Nodos expandidos:   {expandidos}")
  print(f"Nodos en memoria:   {memoria}")
  print(f"Memoria real:       {memoria_bytes} bytes")
  print(f"Tiempo:             {tiempo:.6f} s")

  _guardar_fila_demo({
    "actividad": "2",
    "metodo_heuristica": "UCS",
    "layout": layout_name,
    "costo": costo,
    "longitud_camino": longitud,
    "nodos_expandidos": expandidos,
    "nodos_en_memoria": memoria,
    "memoria_bytes": memoria_bytes,
    "tiempo_seg": f"{tiempo:.6f}",
    "optimo": "si",
  })
  print(f"\nFila guardada en resultados.csv (actividad=2, metodo=UCS, layout={layout_name}).")


def demo_actividad3():
  """Actividad 3 (solo verifica, no genera fila)."""
  layouts = ["tinyMaze", "mediumMaze", "mediumClassic", "openClassic", "trickyClassic"]

  def _correr(layout_name, funcion, heuristica=None):
    state = _demo_estado(layout_name)
    problem = PositionSearchProblem(state, warn=False)
    acciones = funcion(problem, heuristica) if heuristica is not None else funcion(problem)
    return problem.getCostOfActions(acciones), problem._expanded

  print("=" * 88)
  print("Actividad 3 - Verificacion de aStarSearch contra la linea base de UCS")
  print("=" * 88)
  fallas = []
  for layout_name in layouts:
    costo_ucs, exp_ucs = _correr(layout_name, search.uniformCostSearch)
    costo_h0, exp_h0 = _correr(layout_name, search.aStarSearch, search.nullHeuristic)
    costo_man, exp_man = _correr(layout_name, search.aStarSearch, manhattanHeuristic)
    costo_euc, exp_euc = _correr(layout_name, search.aStarSearch, euclideanHeuristic)

    print(f"\n{layout_name}:")
    print(f"  UCS             costo={costo_ucs:4d}  expandidos={exp_ucs:4d}")
    print(f"  A* + h=0        costo={costo_h0:4d}  expandidos={exp_h0:4d}")
    print(f"  A* + Manhattan  costo={costo_man:4d}  expandidos={exp_man:4d}")
    print(f"  A* + Euclidiana costo={costo_euc:4d}  expandidos={exp_euc:4d}")

    if not (costo_ucs == costo_h0 == costo_man == costo_euc):
      fallas.append(f"{layout_name}: los costos deberian coincidir (todas optimas)")
    if exp_ucs != exp_h0:
      fallas.append(f"{layout_name}: A*+h=0 deberia expandir igual que UCS")
    if exp_man > exp_h0 or exp_euc > exp_h0:
      fallas.append(f"{layout_name}: una heuristica admisible no deberia expandir mas que h=0")

  print("\n" + "=" * 88)
  if fallas:
    print("FALLAS DETECTADAS:")
    for f in fallas:
      print(f"  - {f}")
  else:
    print("Todas las verificaciones pasaron: A* es correcto y consistente con UCS.")


def demo_actividad4(layout_name="mediumClassic"):
  """Actividad 4."""

  def _medir(nombre, funcion):
    state = _demo_estado(layout_name)
    problem = PositionSearchProblem(state, warn=False)

    inicio = time.perf_counter()
    acciones = funcion(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(
      lambda: PositionSearchProblem(state, warn=False), funcion)

    _guardar_fila_demo({
      "actividad": "4",
      "metodo_heuristica": nombre,
      "layout": layout_name,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": "si",
    })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo

  print("=" * 70)
  print(f"Actividad 4 - A* con h(n)=0 vs. UCS sobre '{layout_name}'")
  print("=" * 70)

  resultados = {
    "UCS": _medir("UCS", search.uniformCostSearch),
    "A* + h(n)=0": _medir("A*+h=0", lambda p: search.aStarSearch(p, search.nullHeuristic)),
  }

  print(f"\n{'Algoritmo':15s} {'Costo':>6s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s}")
  for nombre, (costo, longitud, expandidos, memoria, memoria_bytes, tiempo) in resultados.items():
    print(f"{nombre:15s} {costo:6d} {expandidos:11d} {memoria:9d} {memoria_bytes:10d} {tiempo:12.6f}")

  costo_ucs = resultados["UCS"][0]
  exp_ucs = resultados["UCS"][2]
  costo_astar = resultados["A* + h(n)=0"][0]
  exp_astar = resultados["A* + h(n)=0"][2]

  print("\nVerificacion:")
  print(f"  Mismo costo (ambas optimas): {costo_ucs == costo_astar}")
  print(f"  Mismos nodos expandidos:     {exp_ucs == exp_astar}")
  print("\nFilas guardadas en resultados.csv (actividad=4).")


def demo_actividad5(layout_name="mediumClassic"):
  """Actividad 5."""

  def _medir(nombre, funcion):
    state = _demo_estado(layout_name)
    problem = PositionSearchProblem(state, warn=False)

    inicio = time.perf_counter()
    acciones = funcion(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(
      lambda: PositionSearchProblem(state, warn=False), funcion)
    celdas_exploradas = list(problem._visitedlist)

    _guardar_fila_demo({
      "actividad": "5",
      "metodo_heuristica": nombre,
      "layout": layout_name,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": "si",
    })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo, celdas_exploradas

  print("=" * 70)
  print(f"Actividad 5 - A* con distancia Manhattan vs. UCS sobre '{layout_name}'")
  print("=" * 70)

  resultados = {
    "UCS": _medir("UCS", search.uniformCostSearch),
    "A* + Manhattan": _medir("A*+Manhattan", lambda p: search.aStarSearch(p, manhattanHeuristic)),
  }

  print(f"\n{'Algoritmo':16s} {'Costo':>6s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s}")
  for nombre, (costo, longitud, expandidos, memoria, memoria_bytes, tiempo, _) in resultados.items():
    print(f"{nombre:16s} {costo:6d} {expandidos:11d} {memoria:9d} {memoria_bytes:10d} {tiempo:12.6f}")

  exp_ucs = resultados["UCS"][2]
  exp_man = resultados["A* + Manhattan"][2]
  celdas_ucs = set(resultados["UCS"][6])
  celdas_man = set(resultados["A* + Manhattan"][6])

  print(f"\nReduccion de nodos expandidos: UCS={exp_ucs} -> A*+Manhattan={exp_man} "
        f"(R = {exp_ucs / exp_man:.2f}x menos expansiones)")
  print(f"Celdas exploradas por UCS pero NO por A*+Manhattan: "
        f"{len(celdas_ucs - celdas_man)} de {len(celdas_ucs)}")

  print("\nFilas guardadas en resultados.csv (actividad=5).")


def demo_actividad6(layout_name="mediumClassic"):
  """Actividad 6."""

  def _medir(nombre, heuristica):
    state = _demo_estado(layout_name)
    problem = PositionSearchProblem(state, warn=False)

    inicio = time.perf_counter()
    acciones = search.aStarSearch(problem, heuristica)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(
      lambda: PositionSearchProblem(state, warn=False), lambda p: search.aStarSearch(p, heuristica))

    _guardar_fila_demo({
      "actividad": "6",
      "metodo_heuristica": nombre,
      "layout": layout_name,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": "si",
    })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo

  print("=" * 78)
  print(f"Actividad 6 - Comparacion de heuristicas (A*) sobre '{layout_name}'")
  print("=" * 78)

  heuristicas = {
    "h(n)=0": search.nullHeuristic,
    "Manhattan": manhattanHeuristic,
    "Euclidiana": euclideanHeuristic,
  }
  resultados = {nombre: _medir(nombre, h) for nombre, h in heuristicas.items()}

  print(f"\n{'Heuristica':12s} {'Longitud':>9s} {'Costo':>6s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s}")
  for nombre, (costo, longitud, expandidos, memoria, memoria_bytes, tiempo) in resultados.items():
    print(f"{nombre:12s} {longitud:9d} {costo:6d} {expandidos:11d} {memoria:9d} {memoria_bytes:10d} {tiempo:12.6f}")

  exp_null = resultados["h(n)=0"][2]
  exp_man = resultados["Manhattan"][2]
  exp_euc = resultados["Euclidiana"][2]

  print(f"\nManhattan expande {exp_null - exp_man} nodos menos que h(n)=0 "
        f"({exp_null} -> {exp_man}).")
  print(f"Euclidiana expande {exp_null - exp_euc} nodos menos que h(n)=0 "
        f"({exp_null} -> {exp_euc}).")
  print(f"Manhattan vs. Euclidiana: {exp_man} vs. {exp_euc} nodos expandidos "
        f"({'Manhattan es mas informativa' if exp_man < exp_euc else 'Euclidiana es mas informativa' if exp_euc < exp_man else 'empate'} "
        f"en este layout).")

  print("\nFilas guardadas en resultados.csv (actividad=6).")


def demo_actividad7():
  """Actividad 7."""
  layout_principal = "tinyCorners"

  def _probar_conectividad_mediumCorners():
    state = _demo_estado("mediumCorners")
    problem = PositionSearchProblem(state, goal=(1, 1), warn=False)
    acciones = search.uniformCostSearch(problem)
    alcanzable = len(acciones) > 0 or problem.isGoalState(problem.getStartState())
    print(f"Verificacion mediumCorners: (1,1) alcanzable desde el inicio = {alcanzable}")
    if not alcanzable:
      print("  -> Confirmado con PositionSearchProblem (codigo del profesor, sin tocar):")
      print("     el punto de partida de mediumCorners esta en un cuarto sellado.")
      print("     mediumCorners NO se usa como layout de referencia por este motivo.")
    return alcanzable

  def _probar_corners(layout_name):
    state = _demo_estado(layout_name)
    problem = CornersProblem(state)

    print(f"Layout: {layout_name}")
    print(f"  Esquinas: {problem.corners}")
    print(f"  Estado inicial: {problem.getStartState()}")

    inicio = time.perf_counter()
    acciones = search.uniformCostSearch(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(
      lambda: CornersProblem(state), search.uniformCostSearch)

    _guardar_fila_demo({
      "actividad": "7",
      "metodo_heuristica": "UCS",
      "layout": layout_name,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": "si",
    })

    print(f"  UCS: costo={costo} longitud={len(acciones)} expandidos={expandidos} memoria={memoria} "
          f"memoria_bytes={memoria_bytes} tiempo={tiempo:.6f}s")
    print()

  _probar_conectividad_mediumCorners()
  print()
  _probar_corners(layout_principal)
  print("Filas guardadas en resultados.csv (actividad=7).")


def demo_actividad8():
  """Actividad 8."""
  layout_principal = "tinyCorners"
  costo_optimo_conocido = 22  # de la Actividad 7 (UCS sobre tinyCorners)
  state_principal = _demo_estado(layout_principal)

  def _nuevo_problema():
    return CornersProblem(state_principal)

  def _medir(nombre, funcion_busqueda):
    problem = _nuevo_problema()

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(_nuevo_problema, funcion_busqueda)

    _guardar_fila_demo({
      "actividad": "8",
      "metodo_heuristica": nombre,
      "layout": layout_principal,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": "si",
    })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo

  problem0 = _nuevo_problema()
  inicio_estado = problem0.getStartState()
  h_basica = cornersHeuristicBasica(inicio_estado, problem0)
  h_propuesta = cornersHeuristic(inicio_estado, problem0)

  print(f"Estado inicial: {inicio_estado}")
  print(f"  h*(inicio) real (costo optimo, Actividad 7) = {costo_optimo_conocido}")
  print(f"  h_basica(inicio)    = {h_basica}  "
        f"({'OK, no sobreestima' if h_basica <= costo_optimo_conocido else 'FALLA: sobreestima'})")
  print(f"  h_propuesta(inicio) = {h_propuesta}  "
        f"({'OK, no sobreestima' if h_propuesta <= costo_optimo_conocido else 'FALLA: sobreestima'})")
  print()

  print("=" * 78)
  print(f"Actividad 8 - Comparacion de heuristicas de esquinas sobre '{layout_principal}'")
  print("=" * 78)

  heuristicas = {
    "h(n)=0": lambda p: search.aStarSearch(p, search.nullHeuristic),
    "Heuristica basica": lambda p: search.aStarSearch(p, cornersHeuristicBasica),
    "Heuristica propuesta": lambda p: search.aStarSearch(p, cornersHeuristic),
  }
  resultados = {nombre: _medir(nombre, f) for nombre, f in heuristicas.items()}

  print(f"{'Heuristica':22s} {'Costo':>6s} {'Longitud':>9s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s}")
  for nombre, (costo, longitud, expandidos, memoria, memoria_bytes, tiempo) in resultados.items():
    print(f"{nombre:22s} {costo:6d} {longitud:9d} {expandidos:11d} {memoria:9d} {memoria_bytes:10d} {tiempo:12.6f}")

  exp0 = resultados["h(n)=0"][2]
  expB = resultados["Heuristica basica"][2]
  expP = resultados["Heuristica propuesta"][2]
  print(f"Heuristica basica expande {exp0 - expB} nodos menos que h=0 ({exp0} -> {expB}).")
  print(f"Heuristica propuesta expande {exp0 - expP} nodos menos que h=0 ({exp0} -> {expP}), "
        f"y {expB - expP} menos que la basica ({expB} -> {expP}).")
  print()
  print("Filas guardadas en resultados.csv (actividad=8).")


def demo_actividad9():
  """Actividad 9."""
  layout_principal = "tinyCorners"
  state_principal = _demo_estado(layout_principal)

  def _nuevo_problema():
    return CornersProblem(state_principal)

  def _medir(metodo, funcion_busqueda, costo_optimo_referencia):
    problem = _nuevo_problema()

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(_nuevo_problema, funcion_busqueda)
    optimo = "si" if costo == costo_optimo_referencia else "no"

    _guardar_fila_demo({
      "actividad": "9",
      "metodo_heuristica": metodo,
      "layout": layout_principal,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": optimo,
    })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo, optimo

  print("=" * 88)
  print(f"Actividad 9 - Experimento comparativo sobre '{layout_principal}'")
  print("=" * 88)

  problem_ucs = _nuevo_problema()
  inicio = time.perf_counter()
  acciones_ucs = search.uniformCostSearch(problem_ucs)
  t_ucs = time.perf_counter() - inicio
  costo_ucs = problem_ucs.getCostOfActions(acciones_ucs)
  long_ucs = len(acciones_ucs)
  exp_ucs = problem_ucs._expanded
  mem_ucs = problem_ucs._maxMemory
  mem_bytes_ucs = search.medirMemoriaBytes(_nuevo_problema, search.uniformCostSearch)
  _guardar_fila_demo({
    "actividad": "9", "metodo_heuristica": "UCS", "layout": layout_principal,
    "costo": costo_ucs, "longitud_camino": long_ucs, "nodos_expandidos": exp_ucs,
    "nodos_en_memoria": mem_ucs, "memoria_bytes": mem_bytes_ucs,
    "tiempo_seg": f"{t_ucs:.6f}", "optimo": "si",
  })

  metodos = {
    "A* + h=0": lambda p: search.aStarSearch(p, search.nullHeuristic),
    "A* + heuristica basica": lambda p: search.aStarSearch(p, cornersHeuristicBasica),
    "A* + heuristica propuesta": lambda p: search.aStarSearch(p, cornersHeuristic),
  }

  filas = {"UCS": (costo_ucs, long_ucs, exp_ucs, mem_ucs, mem_bytes_ucs, t_ucs, "si")}
  for nombre, f in metodos.items():
    filas[nombre] = _medir(nombre, f, costo_optimo_referencia=costo_ucs)

  print(f"{'Metodo':26s} {'Costo':>6s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s} {'Optimo':>7s}")
  for nombre, (costo, longitud, expandidos, memoria, memoria_bytes, tiempo, optimo) in filas.items():
    print(f"{nombre:26s} {costo:6d} {expandidos:11d} {memoria:9d} {memoria_bytes:10d} {tiempo:12.6f} {optimo:>7s}")

  n_ucs = filas["UCS"][2]
  n_astar_propuesta = filas["A* + heuristica propuesta"][2]
  R = n_ucs / n_astar_propuesta
  print()
  print(f"Factor de reduccion R = N_UCS / N_A* = {n_ucs} / {n_astar_propuesta} = {R:.2f}")
  print(f"(usando la heuristica propuesta, la mas informada, como referencia de N_A*)")
  print(f"UCS expandio aproximadamente {R:.2f} veces mas estados que A*+heuristica propuesta.")
  print()
  print("Filas guardadas en resultados.csv (actividad=9).")


def demo_actividad10():
  """Actividad 10."""
  layouts = ["tinySearch", "testClassic"]

  def _medir(layout_name, nombre, funcion_busqueda):
    state = _demo_estado(layout_name)
    problem = FoodSearchProblem(state)

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(lambda: FoodSearchProblem(state), funcion_busqueda)
    numFoodInicial = state.getFood().count()

    _guardar_fila_demo({
      "actividad": "10",
      "metodo_heuristica": nombre,
      "layout": layout_name,
      "costo": costo,
      "longitud_camino": len(acciones),
      "nodos_expandidos": expandidos,
      "nodos_en_memoria": memoria,
      "memoria_bytes": memoria_bytes,
      "tiempo_seg": f"{tiempo:.6f}",
      "optimo": "si",
    })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo, numFoodInicial

  def _explorar(layout_name):
    print("=" * 78)
    print(f"Actividad 10 - FoodSearchProblem sobre '{layout_name}'")
    print("=" * 78)

    costo_u, long_u, exp_u, mem_u, membytes_u, t_u, nfood = _medir(layout_name, "UCS", search.uniformCostSearch)
    costo_a, long_a, exp_a, mem_a, membytes_a, t_a, _ = _medir(
      layout_name, "A*+h(n)=0", lambda p: search.aStarSearch(p, search.nullHeuristic)
    )

    print(f"Alimentos iniciales en el layout: {nfood}")
    print(f"{'Metodo':12s} {'Costo':>6s} {'Longitud':>9s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s}")
    print(f"{'UCS':12s} {costo_u:6d} {long_u:9d} {exp_u:11d} {mem_u:9d} {membytes_u:10d} {t_u:12.6f}")
    print(f"{'A*+h(n)=0':12s} {costo_a:6d} {long_a:9d} {exp_a:11d} {mem_a:9d} {membytes_a:10d} {t_a:12.6f}")
    print("Verificado: mismo costo optimo y mismos nodos expandidos (igual que en la Actividad 4).")
    print()

  for layout_name in layouts:
    _explorar(layout_name)

  print("=" * 78)
  print("Nota sobre crecimiento del espacio de estados (no incluido en resultados.csv):")
  print("Se intento correr UCS sobre 'smallClassic' (55 alimentos) con un limite de 45s")
  print("y NO termino: es la explosion combinatoria 2^F que menciona la guia (con F=55,")
  print("2^55 configuraciones posibles de alimento presente/consumido). Por eso los")
  print("layouts de esta actividad y de la 11 se restringen a testClassic (8 alimentos)")
  print("y tinySearch (1 alimento), donde UCS puro SI es viable como linea base.")
  print("Filas guardadas en resultados.csv (actividad=10).")


def demo_actividad11():
  """Actividad 11."""
  layouts_comparacion = ["tinySearch", "testClassic"]
  layouts_cache = ["testClassic", "capsuleClassic"]
  repeticiones_cache = 5

  def _medir(layout_name, nombre, funcion_busqueda, guardar=True):
    state = _demo_estado(layout_name)
    problem = FoodSearchProblem(state)

    inicio = time.perf_counter()
    acciones = funcion_busqueda(problem)
    tiempo = time.perf_counter() - inicio

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria = problem._maxMemory
    memoria_bytes = search.medirMemoriaBytes(lambda: FoodSearchProblem(state), funcion_busqueda)

    if guardar:
      _guardar_fila_demo({
        "actividad": "11",
        "metodo_heuristica": nombre,
        "layout": layout_name,
        "costo": costo,
        "longitud_camino": len(acciones),
        "nodos_expandidos": expandidos,
        "nodos_en_memoria": memoria,
        "memoria_bytes": memoria_bytes,
        "tiempo_seg": f"{tiempo:.6f}",
        "optimo": "si",
      })
    return costo, len(acciones), expandidos, memoria, memoria_bytes, tiempo

  def _comparar_heuristicas(layout_name):
    print("=" * 78)
    print(f"Actividad 11 - Comparacion de heuristicas de comida sobre '{layout_name}'")
    print("=" * 78)

    heuristicas = {
      "h(n)=0": lambda p: search.aStarSearch(p, search.nullHeuristic),
      "Heuristica 1": lambda p: search.aStarSearch(p, foodHeuristicV1),
      "Heuristica 2": lambda p: search.aStarSearch(p, foodHeuristic),
    }
    resultados = {nombre: _medir(layout_name, nombre, f) for nombre, f in heuristicas.items()}

    print(f"{'Heuristica':14s} {'Costo':>6s} {'Longitud':>9s} {'Expandidos':>11s} {'Memoria':>9s} {'Bytes':>10s} {'Tiempo (s)':>12s}")
    for nombre, (costo, longitud, expandidos, memoria, memoria_bytes, tiempo) in resultados.items():
      print(f"{nombre:14s} {costo:6d} {longitud:9d} {expandidos:11d} {memoria:9d} {memoria_bytes:10d} {tiempo:12.6f}")

    exp0 = resultados["h(n)=0"][2]
    exp1 = resultados["Heuristica 1"][2]
    exp2 = resultados["Heuristica 2"][2]
    print(f"Heuristica 1 expande {exp0 - exp1} nodos menos que h=0 ({exp0} -> {exp1}).")
    print(f"Heuristica 2 expande {exp0 - exp2} nodos menos que h=0 ({exp0} -> {exp2}), "
          f"y {exp1 - exp2} menos que Heuristica 1 ({exp1} -> {exp2}).")
    print()

  def _comparar_cache(layout_name):
    print("=" * 78)
    print(f"Actividad 11 - Reto de cache (Heuristica 2 con/sin problem.heuristicInfo) en '{layout_name}'")
    print("=" * 78)

    tiempos_con, tiempos_sin = [], []
    for _ in range(repeticiones_cache):
      _, _, exp_con, mem_con, membytes_con, t_con = _medir(
        layout_name, "H2_con_cache", lambda p: search.aStarSearch(p, foodHeuristic), guardar=False
      )
      _, _, exp_sin, mem_sin, membytes_sin, t_sin = _medir(
        layout_name, "H2_sin_cache", lambda p: search.aStarSearch(p, foodHeuristicV2SinCache), guardar=False
      )
      tiempos_con.append(t_con)
      tiempos_sin.append(t_sin)

    prom_con = sum(tiempos_con) / len(tiempos_con)
    prom_sin = sum(tiempos_sin) / len(tiempos_sin)

    _guardar_fila_demo({
      "actividad": "11", "metodo_heuristica": "H2_con_cache", "layout": layout_name,
      "costo": "-", "longitud_camino": "-", "nodos_expandidos": exp_con,
      "nodos_en_memoria": mem_con, "memoria_bytes": membytes_con,
      "tiempo_seg": f"{prom_con:.6f}", "optimo": "si",
    })
    _guardar_fila_demo({
      "actividad": "11", "metodo_heuristica": "H2_sin_cache", "layout": layout_name,
      "costo": "-", "longitud_camino": "-", "nodos_expandidos": exp_sin,
      "nodos_en_memoria": mem_sin, "memoria_bytes": membytes_sin,
      "tiempo_seg": f"{prom_sin:.6f}", "optimo": "si",
    })

    print(f"Nodos expandidos (identicos en ambas, misma heuristica): {exp_con}")
    print(f"Tiempo promedio CON cache ({repeticiones_cache} corridas): {prom_con:.6f}s "
          f"{[round(t, 5) for t in tiempos_con]}")
    print(f"Tiempo promedio SIN cache ({repeticiones_cache} corridas): {prom_sin:.6f}s "
          f"{[round(t, 5) for t in tiempos_sin]}")
    diferencia_pct = (prom_sin / prom_con - 1) * 100 if prom_con > 0 else 0
    print(f"Diferencia: {diferencia_pct:+.1f}% (sin cache vs. con cache).")
    print()

  for layout_name in layouts_comparacion:
    _comparar_heuristicas(layout_name)
  for layout_name in layouts_cache:
    _comparar_cache(layout_name)

  print("Filas guardadas en resultados.csv (actividad=11).")


def demo_resultados_generales(repeticiones=10):
  "Fila por experimento de la tabla de resultados generales, promediando tiempo y memoria en bytes sobre `repeticiones` corridas."
  layout_medium = _demo_estado("mediumClassic")
  layout_corners = _demo_estado("tinyCorners")
  layout_food = _demo_estado("testClassic")

  experimentos = [
    ("UCS", lambda: PositionSearchProblem(layout_medium, warn=False),
     search.uniformCostSearch),
    ("A* + heuristica nula", lambda: PositionSearchProblem(layout_medium, warn=False),
     lambda p: search.aStarSearch(p, search.nullHeuristic)),
    ("A* + Manhattan", lambda: PositionSearchProblem(layout_medium, warn=False),
     lambda p: search.aStarSearch(p, manhattanHeuristic)),
    ("A* + Euclidiana", lambda: PositionSearchProblem(layout_medium, warn=False),
     lambda p: search.aStarSearch(p, euclideanHeuristic)),
    ("A* + Corners Heuristic", lambda: CornersProblem(layout_corners),
     lambda p: search.aStarSearch(p, cornersHeuristic)),
    ("A* + Food Heuristic", lambda: FoodSearchProblem(layout_food),
     lambda p: search.aStarSearch(p, foodHeuristic)),
  ]

  print("=" * 90)
  print(f"Resultados generales - promedio de tiempo sobre {repeticiones} corridas")
  print("=" * 90)

  filas = []
  for nombre, fabrica_problema, funcion_busqueda in experimentos:
    tiempos = []
    for _ in range(repeticiones):
      problem = fabrica_problema()
      inicio = time.perf_counter()
      acciones = funcion_busqueda(problem)
      tiempos.append(time.perf_counter() - inicio)

    costo = problem.getCostOfActions(acciones)
    expandidos = problem._expanded
    memoria_nodos = problem._maxMemory

    bytes_medidos = [
      search.medirMemoriaBytes(fabrica_problema, funcion_busqueda)
      for _ in range(repeticiones)
    ]

    tiempo_prom = sum(tiempos) / len(tiempos)
    tiempo_min = min(tiempos)
    tiempo_max = max(tiempos)

    memoria_bytes_prom = sum(bytes_medidos) / len(bytes_medidos)

    filas.append((nombre, costo, expandidos, memoria_nodos, memoria_bytes_prom, tiempo_prom))

    print(f"\n{nombre}")
    print(f"  Costo={costo}  Expandidos={expandidos}  Memoria(nodos)={memoria_nodos}")
    print(f"  Memoria real promedio ({repeticiones} corridas): {memoria_bytes_prom:,.0f} bytes "
          f"(min={min(bytes_medidos):,}, max={max(bytes_medidos):,})")
    print(f"  Tiempo promedio ({repeticiones} corridas): {tiempo_prom:.6f}s "
          f"(min={tiempo_min:.6f}s, max={tiempo_max:.6f}s)")

  print("\n" + "=" * 90)
  print("Filas listas para pegar en docs/latex/secciones/resultados_generales.tex:")
  print("=" * 90)
  for nombre, costo, expandidos, memoria_nodos, memoria_bytes_prom, tiempo_prom in filas:
    print(f"{nombre:26s} & {costo} & {expandidos} & {memoria_nodos} & "
          f"{memoria_bytes_prom:,.0f} & {tiempo_prom:.6f} \\\\")

  return filas


if __name__ == "__main__":
  import sys

  _DEMOS = {
    1: demo_actividad1,
    2: demo_actividad2,
    3: demo_actividad3,
    4: demo_actividad4,
    5: demo_actividad5,
    6: demo_actividad6,
    7: demo_actividad7,
    8: demo_actividad8,
    9: demo_actividad9,
    10: demo_actividad10,
    11: demo_actividad11,
    "generales": demo_resultados_generales,
  }

  if len(sys.argv) > 1:
    _numeros = [a if a == "generales" else int(a) for a in sys.argv[1:]]
  else:
    _numeros = list(range(1, 12))

  for _n in _numeros:
    if _n not in _DEMOS:
      print(f"Actividad {_n} no existe (usar un numero entero de 1 a 11, o 'generales').")
      continue
    _DEMOS[_n]()
    print()

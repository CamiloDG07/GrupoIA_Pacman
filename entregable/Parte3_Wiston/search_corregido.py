"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).

=====================================================================
REVISION (Wiston, Parte 3 del grupo) sobre la version que mando el
companero encargado de la Parte 1 (Actividades 1-6):
=====================================================================

Se encontraron y corrigieron DOS problemas reales, verificados
ejecutando el archivo tal cual llego (no solo leyendolo):

1. uniformCostSearch (Actividad 2) NO estaba implementada: solo tenia
   "util.raiseNotDefined()", que en este proyecto especifico hace
   "sys.exit(1)" -- es decir, TERMINA TODO EL PROCESO DE PYTHON apenas
   se llama, no lanza una excepcion que se pueda capturar. Confirmado
   corriendola: el proceso termina con exit code 1 imprimiendo
   "Method not implemented: uniformCostSearch". Se implemento aqui,
   seleccionando exactamente el mismo patron de aStarSearch que ya
   traia el archivo (diccionario "explored" con re-apertura de nodos),
   para que el archivo completo quede en un unico estilo consistente.

2. aStarSearch SI estaba implementada y el algoritmo en si es correcto
   (frontera de prioridad + prueba de meta al extraer + diccionario
   "explored" que permite reabrir un estado si se encuentra un costo
   mejor), pero le faltaba un contador de desempate en la tupla de la
   frontera. Sin el, en cuanto dos entradas empatan en prioridad,
   util.PriorityQueue (que usa heapq SIN ningun tiebreaker propio,
   ver util.py) compara el resto de la tupla -- (estado, acciones,
   costo) --, y esa comparacion revienta con
       TypeError: '<' not supported between instances of 'Grid' and 'Grid'
   apenas el estado incluye un Grid no comparable, como el foodGrid de
   FoodSearchProblem (las Actividades 10 y 11, que son justo la Parte
   3). Confirmado: sin el fix, aStarSearch(problem, nullHeuristic)
   sobre el layout testClassic con FoodSearchProblem revienta con ese
   error exacto (funcionaba en PositionSearchProblem porque ahi el
   estado es (x,y), siempre comparable, por eso el bug no se notaba
   antes). Con el fix (un contador entero unico como primer elemento
   de cada tupla), aStarSearch corre bien sobre FoodSearchProblem:
   testClassic da costo=16, expandidos=2598, exactamente igual que con
   la implementacion propia de la Parte 3.

Todo lo demas del archivo (SearchProblem, tinyMazeSearch,
depthFirstSearch/breadthFirstSearch sin implementar -- no las pide
ninguna de las 11 actividades de la guia --, nullHeuristic) se dejo
tal cual, sin tocar.
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  util.raiseNotDefined()

def uniformCostSearch(problem):
  """
  Search the node of least total cost first.

  [Corregido -- ver nota al inicio del archivo] No estaba implementada;
  se completo usando el mismo patron que ya traia aStarSearch en este
  archivo: frontera de prioridad + diccionario "explored" que guarda el
  mejor costo conocido por estado y permite reabrirlo (volver a
  expandirlo) si aparece un camino mas barato. La prioridad es
  simplemente g(n) (el costo acumulado), sin ninguna heuristica.

  Incluye el mismo contador de desempate (tieBreaker) que aStarSearch,
  necesario por la misma razon (ver nota al inicio del archivo).
  """
  from util import PriorityQueue

  frontier = PriorityQueue()
  explored = {}

  start_state = problem.getStartState()
  contador = 0
  frontier.push((contador, start_state, [], 0), 0)

  while not frontier.isEmpty():
      _, current_state, actions, current_g = frontier.pop()

      if problem.isGoalState(current_state):
          return actions

      if current_state not in explored or current_g < explored[current_state]:
          explored[current_state] = current_g

          for successor, action, stepCost in problem.getSuccessors(current_state):
              new_g = current_g + stepCost
              new_actions = actions + [action]
              contador += 1
              frontier.push((contador, successor, new_actions, new_g), new_g)

  return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  """
  Search the node that has the lowest combined cost and heuristic first.

  [Corregido -- ver nota al inicio del archivo] Se agrego un contador de
  desempate (tieBreaker) como primer elemento de cada tupla de la
  frontera. El resto del algoritmo (frontera de prioridad con f(n) =
  g(n) + h(n), prueba de meta al extraer el nodo, diccionario
  "explored" con re-apertura de nodos si se encuentra un costo mejor)
  se dejo exactamente igual: es un patron distinto al de "podar antes
  de insertar" (bestCost) que usa la implementacion propia de la Parte
  3, pero igual de correcto para heuristicas admisibles y consistentes
  como las de este proyecto (Manhattan, Euclidiana, foodHeuristic).
  """
  from util import PriorityQueue

  frontier = PriorityQueue()
  explored = {}

  start_state = problem.getStartState()
  contador = 0
  start_g = 0
  start_h = heuristic(start_state, problem)
  start_f = start_g + start_h

  frontier.push((contador, start_state, [], start_g), start_f)

  while not frontier.isEmpty():
      _, current_state, actions, current_g = frontier.pop()

      if problem.isGoalState(current_state):
          return actions

      if current_state not in explored or current_g < explored[current_state]:
          explored[current_state] = current_g

          for successor, action, stepCost in problem.getSuccessors(current_state):
              new_g = current_g + stepCost
              new_actions = actions + [action]
              new_f = new_g + heuristic(successor, problem)
              contador += 1
              frontier.push((contador, successor, new_actions, new_g), new_f)

  return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

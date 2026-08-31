"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
      
def uniformCostSearch(problem):
  """
  Search the node of least total cost first.

  Actividad 2 del taller "Busqueda Informada con Pac-Man".

  UCS es una busqueda en grafo: la frontera es una cola de prioridad
  (util.PriorityQueue) ordenada por g(n), el costo acumulado real desde el
  estado inicial hasta n (no se usa ninguna heuristica, h(n) = 0 siempre).
  En cada paso se extrae el estado con menor g(n) conocido; si ya es meta,
  se retorna el plan que llego hasta el. Si no, se expande (esto es lo que
  incrementa problem._expanded, la metrica de "nodos expandidos").

  Se lleva un diccionario bestCost con el mejor costo conocido para cada
  estado visitado. Como util.PriorityQueue no permite bajar la prioridad de
  un elemento ya insertado (no tiene decrease-key), cuando se encuentra un
  camino mas barato hacia un estado simplemente se vuelve a insertar ese
  estado con su nuevo costo; las copias "viejas" que puedan quedar en la
  cola se descartan al extraerlas (ver el chequeo de abajo), en vez de
  expandirlas de nuevo.

  Contador de desempate (tieBreaker): util.PriorityQueue usa heapq, que
  guarda tuplas (prioridad, item). Si dos entradas tienen la MISMA
  prioridad, heapq compara "item" para decidir el orden, y en problemas
  donde el estado no es simplemente (x, y) sino que incluye estructuras no
  comparables --como el Grid de comida en FoodSearchProblem, Actividad
  10-11-- esa comparacion revienta con un TypeError. Por eso cada elemento
  de la frontera lleva un contador entero unico y creciente en la primera
  posicion de la tupla: como los contadores nunca se repiten, heapq nunca
  necesita mirar mas alla de ellos para resolver un empate.
  """
  frontier = util.PriorityQueue()

  startState = problem.getStartState()
  contador = 0
  # Cada elemento de la frontera es (contador, estado, acciones, g(n)).
  frontier.push((contador, startState, [], 0), 0)

  # Mejor costo g(n) conocido hasta ahora para cada estado.
  bestCost = {startState: 0}

  while not frontier.isEmpty():
    _, state, actions, cost = frontier.pop()

    # Si ya existe un camino mas barato registrado para este estado,
    # esta es una entrada obsoleta de la cola: se descarta sin expandir.
    if cost > bestCost.get(state, float('inf')):
      continue

    # Prueba de objetivo ANTES de expandir (evita expandir de mas).
    if problem.isGoalState(state):
      return actions

    for successor, action, stepCost in problem.getSuccessors(state):
      newCost = cost + stepCost
      # Solo nos interesa este sucesor si mejora el mejor costo conocido.
      if newCost < bestCost.get(successor, float('inf')):
        bestCost[successor] = newCost
        contador += 1
        frontier.push((contador, successor, actions + [action], newCost), newCost)

  # Frontera vacia sin encontrar meta: no existe solucion.
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

  Actividad 3 del taller "Busqueda Informada con Pac-Man".

  Es el mismo esqueleto de busqueda en grafo que uniformCostSearch (misma
  frontera con util.PriorityQueue, mismo diccionario bestCost para no
  reexpandir un estado cuando ya se conoce un camino mas barato hacia el, y
  el mismo goal-test al extraer el nodo de la frontera). La UNICA diferencia
  es la prioridad usada para ordenar la frontera:

      UCS:  prioridad = g(n)
      A*:   prioridad = g(n) + h(n) = f(n)

  Con heuristic = nullHeuristic (h(n) = 0 siempre), f(n) = g(n) y A* se
  comporta exactamente igual que UCS (Actividad 4). Con una heuristica
  admisible y consistente (Manhattan, Euclidiana, etc.) A* sigue siendo
  optimo, pero prioriza explorar los estados que ademas de tener bajo costo
  acumulado, parecen estar mas cerca del objetivo.

  Igual que en uniformCostSearch, se agrega un contador de desempate
  (tieBreaker) en la tupla de la frontera: sin el, heapq revienta con
  TypeError apenas dos entradas empatan en prioridad y el estado incluye
  algo no comparable (el Grid de comida en FoodSearchProblem, Actividad
  10-11).
  """
  frontier = util.PriorityQueue()

  startState = problem.getStartState()
  contador = 0
  startPriority = 0 + heuristic(startState, problem)  # f = g + h, g = 0
  frontier.push((contador, startState, [], 0), startPriority)

  # Mejor costo g(n) conocido hasta ahora para cada estado (igual que UCS;
  # la heuristica NO se guarda aqui porque no hace falta: se recalcula al
  # generar cada sucesor).
  bestCost = {startState: 0}

  while not frontier.isEmpty():
    _, state, actions, cost = frontier.pop()

    # Entrada obsoleta de la cola (ya se encontro un g(n) mejor): se
    # descarta sin expandir, igual que en UCS.
    if cost > bestCost.get(state, float('inf')):
      continue

    # Prueba de objetivo ANTES de expandir.
    if problem.isGoalState(state):
      return actions

    for successor, action, stepCost in problem.getSuccessors(state):
      newCost = cost + stepCost
      if newCost < bestCost.get(successor, float('inf')):
        bestCost[successor] = newCost
        contador += 1
        priority = newCost + heuristic(successor, problem)  # f(n) = g(n) + h(n)
        frontier.push((contador, successor, actions + [action], newCost), priority)

  # Frontera vacia sin encontrar meta: no existe solucion.
  return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
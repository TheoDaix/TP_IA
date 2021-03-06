# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""

		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

class Node:
	def __init__(self, state, parent,  parentAction, cost = 1):
		self.state = state
		self.parent = parent
		self.parentAction = parentAction
		self.cost = cost
		
	def __eq__(self,other): 
		if not isinstance(other, Node):
			return False
		return self.state==other.state 

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	
	start = Node(problem.getStartState(), None,None,0)
	return recursiveDfs(start, problem,[problem.getStartState()])[1:]
			
def recursiveDfs(node, problem,exploredSet):
	if (problem.isGoalState(node.state)):
		return [node.parentAction]
	else:
		for child in problem.getSuccessors(node.state):
			(childState, action, cost) = child
			if not(childState in exploredSet):
				exploredSet.append(childState)  
				childNode = Node(childState, node, action )
				result = recursiveDfs(childNode, problem,exploredSet) 
				if result != None:
					return [node.parentAction] + result

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	start = Node(problem.getStartState(), None,None,0)
	frontier = util.Queue()
	frontier.push(start)
	exploredSet = []
	while not(frontier.isEmpty()):
		node = frontier.pop()
		if (problem.isGoalState(node.state)):
			return solution(node)
		else:
			exploredSet.append(node.state)
			for child in problem.getSuccessors(node.state): 
				(childState, action, cost) = child
				childNode = Node(childState, node, action )
				if not(childState in exploredSet or childNode in frontier.list): 
					frontier.push(childNode)
		
def solution(node):
	if node.parent == None:
		return []
	else:
		return solution(node.parent)+ [node.parentAction]
	
def coreCostSearch(problem, heuristic):
	def heuristicCost(node):
		return node.cost + heuristic(node.state,problem)
	start = Node(problem.getStartState(), None,None,0)
	frontier = util.PriorityQueue()
	frontier.push(start,heuristicCost(start))
	exploredSet = []
	while not(frontier.isEmpty()):
		node = frontier.pop()
		if (problem.isGoalState(node.state)):
			return solution(node)
		else:
			exploredSet.append(node.state)
			for child in problem.getSuccessors(node.state): 
				(childState, action, cost) = child
				childNode = Node(childState, node, action, node.cost + cost)
				if not(childState in exploredSet):
					frontier.update(childNode,heuristicCost(childNode))	

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	return coreCostSearch(problem,nullHeuristic)
				

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	return coreCostSearch(problem, heuristic)	

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

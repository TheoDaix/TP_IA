# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
      
        if action == "Stop":
                return -float("inf")    
            
        score = successorGameState.getScore()/10
        
        for capsule in successorGameState.getCapsules():
            if manhattanDistance(capsule,newPos)==0:
                return float("inf")
                
        safe = True
        for newGhostTime in newScaredTimes:
            safe = safe and (newGhostTime != 0)
            
        distFoods = [manhattanDistance(newPos,food) for food in newFood.asList()]
       
        if len(distFoods)==0:
            return float("inf")
        distMin = min(distFoods)
        
        score+= 1/(distMin)    
        
        if not(safe):            
            ghostDist= None
            for ghost in newGhostStates:
                if ghostDist == None or ghostDist > manhattanDistance(newPos,ghost.getPosition()):
                        ghostDist = manhattanDistance(newPos,ghost.getPosition())
            
            if ghostDist <= 1:
                return -float("inf")
            
            
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def terminalTest(gameState,cnt=0):
            return gameState.isWin() or gameState.isLose() or self.depth == cnt
            
        def maxValue(gameState,cnt=0):
            if terminalTest(gameState,cnt):
                return self.evaluationFunction(gameState)
            else:
                return max([minValue(gameState.generateSuccessor(0,a),1,cnt) for a in gameState.getLegalActions(0)])
        
        def minValue(gameState,i=1,cnt=0):
            if terminalTest(gameState,cnt):
                return self.evaluationFunction(gameState)
            elif i == gameState.getNumAgents()-1:
                return min ([maxValue(gameState.generateSuccessor(i,a),cnt+1) for a in gameState.getLegalActions(i)])
            else:
                return min([minValue(gameState.generateSuccessor(i,a),i+1,cnt) for a in gameState.getLegalActions(i)])

        bestAction = "Stop"
        bestScore= -float("inf")
        for a in gameState.getLegalActions(0):
            tmp = minValue(gameState.generateSuccessor(0,a))
            if tmp>=bestScore:
                bestAction = a
                bestScore = tmp
        return bestAction
               
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def terminalTest(gameState, cnt=0):
            return gameState.isWin() or gameState.isLose() or self.depth == cnt

        def maxValue(gameState,alpha,beta, cnt=0):
            if terminalTest(gameState, cnt):
                return self.evaluationFunction(gameState)
                
            v = -float("inf")
            for a in gameState.getLegalActions(0):
                v = max(v,minValue(gameState.generateSuccessor(0, a),
                                    alpha,beta, 1, cnt))
                if v > beta:
                    return v
                alpha = max(alpha,v)
            return v

        def minValue(gameState,alpha,beta, i=1, cnt=0):
            if terminalTest(gameState, cnt):
                return self.evaluationFunction(gameState)

            v = float("inf")
            for a in gameState.getLegalActions(i):
                if i == gameState.getNumAgents() - 1:
                    v = min(v,maxValue(gameState.generateSuccessor(i, a),
                                    alpha,beta, cnt+1))
                else:
                    v = min(v,minValue(gameState.generateSuccessor(i, a),
                                        alpha,beta, i+1, cnt))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
                
        bestAction = None
        alpha = -float("inf")
        beta = float("inf")
        v= -float("inf")
        for a in gameState.getLegalActions(0):
            newVal = minValue(gameState.generateSuccessor(0, a),alpha,
                           beta)
            if v <= newVal:
                v = newVal
                bestAction = a
            if v >= beta :
                return bestAction

            alpha = max(alpha,v)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def avg(l):
            cnt =0
            for i in l:
                cnt+=i
            return float(cnt)/float(len(l))
        def terminalTest(gameState,cnt=0):
            return gameState.isWin() or gameState.isLose() or self.depth == cnt
            
        def maxValue(gameState,cnt=0):
            if terminalTest(gameState,cnt):
                return self.evaluationFunction(gameState)
            else:
                return max([minValue(gameState.generateSuccessor(0,a),1,cnt) for a in gameState.getLegalActions(0)])
        
        def minValue(gameState,i=1,cnt=0):
            if terminalTest(gameState,cnt):
                return self.evaluationFunction(gameState)
            elif i == gameState.getNumAgents()-1:
                return  avg([maxValue(gameState.generateSuccessor(i,a),cnt+1) for a in gameState.getLegalActions(i)])
            else:
                return avg([minValue(gameState.generateSuccessor(i,a),i+1,cnt) for a in gameState.getLegalActions(i)])

        bestAction = None
        bestScore= -float("inf")
        for a in gameState.getLegalActions(0):
            tmp = minValue(gameState.generateSuccessor(0,a))
            if tmp>=bestScore :
                bestAction = a
                bestScore = tmp
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Si on se trouve dans un etat gagnant, alors on met un score infini. Si les fantomes sont effrayes, on incremente le score.
                    Si les fantomes ne sont pas effrayes et qu'on est proche d'eux, alors l'etat a un score -inf. On enleve au score un poids
                    en fonction du nombre de boules restantes et on lui ajoute un poids en fonction de la proximite des nourritures.
    """
    "*** YOUR CODE HERE ***"
    gs = currentGameState
    ghostStates = gs.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    pacmanPos = gs.getPacmanPosition()
    score = gs.getScore()

    if gs.isWin():
        return score
    if all(time !=0 for time in scaredTimes):
        score+= 10
    elif any(manhattanDistance(pacmanPos,ghostPos) <=1 for ghostPos in gs.getGhostPositions()):
        return -float("inf")
    
    score+= max([1./manhattanDistance(pacmanPos,food) for food in gs.getFood().asList()])
    score-= gs.getNumFood()
    return score
    
# Abbreviation
better = betterEvaluationFunction


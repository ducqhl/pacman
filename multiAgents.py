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
        newPacmanPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        MIN_SAFETY_DISTANCE = 1
        FOOD_SCORE = 100
        TIME_LOST = 10
        A_BIG_NUMBER = 1000
		
        ghost_pos_list = currentGameState.getGhostPositions()
        
        #Heurestic score of state-if-action
        heurestic = successorGameState.getScore();

                      
        #### when ghost can eat pacman ###
        #get index of closest ghost
        closest_ghost_distance = ("inf")
        closest_ghost_index = 0
        for i in range(0,len(ghost_pos_list)):
            ghost_distance = manhattanDistance(ghost_pos_list[i], newPacmanPos)
            if (ghost_distance < closest_ghost_distance):
                closest_ghost_distance = ghost_distance
                closest_ghost_index = i

        #don't care about ghost until ghost is too closet and it not scared of pacman
        closest_ghost_is_scared = newScaredTimes[closest_ghost_index]
        ghost_closest = ghost_pos_list[closest_ghost_index]
        if(closest_ghost_distance <= MIN_SAFETY_DISTANCE) and (closest_ghost_distance != 0) and (closest_ghost_is_scared == 0): 
            #closest more low, (MIN_SAFETY_DISTANCE/closest_ghost_distance) more increase
            heurestic -= (MIN_SAFETY_DISTANCE/closest_ghost_distance) * A_BIG_NUMBER
        
        #### when ghost is scared of pacman ####
        #REVENGE time was gone =_- 
        #let pacman search for scared ghost and eat them all          
        if closest_ghost_is_scared != 0 : 
            #(A_BIG_NUMBER/closest_ghost_distance)is more increase when ghost is more close
            heurestic += A_BIG_NUMBER/closest_ghost_distance;     
                
        #get closetFoods
        foodList = newFood.asList()
        if (foodList != []) :
            closest_Food_distance = ("inf")
            for foodPos in foodList:
                pos_vector = manhattanDistance(foodPos, newPacmanPos)
                if (pos_vector < closest_Food_distance):
                    closest_Food_distance = pos_vector
            
            #heurestic more decrease when food is further 
            heurestic -=  closest_Food_distance
        
		#this action make pacman eat food 
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            heurestic += FOOD_SCORE
		#score lost when time is gone
        if action == Directions.STOP:
            heurestic -= TIME_LOST

        return heurestic

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
                PACMAN_INDEX = 0
        #call max_funtion for best action of pacman
        score, action = self.max_function(gameState,PACMAN_INDEX)
        return action

    #return heuristic value of agent(index) will gain in a gameState        
    def value(self, gameState, agentIndex):
        #agentIndex reach out of depth  
        if agentIndex == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState), "noMove";
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore(), "noMove";
             
        if agentIndex % gameState.getNumAgents() == 0:
            #agentIndex of PACMAN       
            return self.max_function(gameState, agentIndex);
        else :
            #agentIndex of GHOST
            return self.min_function(gameState, agentIndex);
            
    def max_function(self, gameState, agentIndex):
        agentStep = agentIndex % gameState.getNumAgents()  #in case if depth > 1, PACMAN plays more than 1 times
        acts = gameState.getLegalActions(agentStep);       
        
        max_score = float("-inf")
        best_act = acts[0]
        
        for a in acts :
            stateIfAction = gameState.generateSuccessor(agentStep,a)
            score, action = self.value(stateIfAction, agentIndex + 1)
            if score > max_score:
                max_score = score
                best_act = a
        return [max_score,best_act]
        
    def min_function(self, gameState, agentIndex):     
        agentStep = agentIndex % gameState.getNumAgents()  #in case if depth > 1, GHOST plays more than 1 times  
        acts = gameState.getLegalActions(agentStep);
        min_score = float("inf")
        worst_act = acts[0]
        for a in acts :
            stateIfAction = gameState.generateSuccessor(agentStep,a)
            score, action = self.value(stateIfAction, agentIndex+1)
            if score < min_score:
                min_score = score
                worst_act = a
        return [min_score,worst_act]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
	PACMAN_INDEX = 0      
        alpha = float('-inf') #max score of pacman can reach 
        beta  =  float('inf') #min score of ghost can make
        
        #call max_funtion for best action of pacman
        score, action= self.max_function(gameState,PACMAN_INDEX, alpha, beta)
        return action

    #return heuristic value of agent(index) will gain in a gameState        
    def value(self, gameState, agentIndex, alpha, beta):
        #agentIndex reach out of depth  
        if agentIndex == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState), "noMove"
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore(), "noMove"
             
        if agentIndex % gameState.getNumAgents() == 0:
            #agentIndex of PACMAN       
            return self.max_function(gameState, agentIndex, alpha, beta);
        else :
            #agentIndex of GHOST
            return self.min_function(gameState, agentIndex, alpha, beta);
            
    def max_function(self, gameState, agentIndex, alpha, beta):
        agentStep = agentIndex % gameState.getNumAgents()  #in case if depth > 1, PACMAN plays more than 1 times
        acts = gameState.getLegalActions(agentStep);       
        
        max_score = float("-inf")
        best_act = acts[0]
        nextAgent =  agentIndex + 1
        
        for act in acts :
            stateIfAction = gameState.generateSuccessor(agentStep,act)           
            score, action = self.value(stateIfAction, nextAgent, alpha, beta)
            
            if score > max_score:
                max_score = score
                best_act = act           
            if score > beta: 
                #the min_function call this max_function will nerver choose this action
                #because them can chosse a worse action (in case orther max_function has lower score)
                return max_score, best_act         
            if score > alpha:
                #save a highest value can reached up to date
                #use it for prunne (min_function)- branches, which definitely can not gives back higher scores
                alpha = score
        return max_score, best_act
        
    def min_function(self, gameState, agentIndex, alpha, beta):     
        agentStep = agentIndex % gameState.getNumAgents()  #in case if depth > 1, GHOST plays more than 1 times  
        acts = gameState.getLegalActions(agentStep);
        min_score = float("inf")
        worst_act = acts[0]
        nextAgent = agentIndex + 1
        for act in acts :
            stateIfAction = gameState.generateSuccessor(agentStep,act)           
            score, action = self.value(stateIfAction, nextAgent, alpha, beta)
            if score < min_score:
                min_score = score
                worst_act = act
            if score < alpha : 
                #the max_function call this min_function will nerver choose this action
                #because them can chosse a better action (in case orther min_function gives back higher score)
                return min_score,worst_act 
            if beta > score:
                #save a lowest value can make up to date
                #use it for prunne (max_function)- branches, which definitely can not gives back lower scores
                beta = score
            
        return min_score,worst_act 
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


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
import random




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
        #print 'Successor game state:',successorGameState
        newPos = successorGameState.getPacmanPosition()
        #print 'New position:',newPos
        newFood = successorGameState.getFood()

        newGhostStates = successorGameState.getGhostStates()
        print 'gs',newGhostStates

        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print newFood
        #print newPos[0]
        optimal_food=[]
        optimal_ghost=[]
        food= currentGameState.getFood().asList()
        ghost=successorGameState.getGhostPositions()

        for f in food:
              optimal_food.append(manhattanDistance(newPos,f))

        a=min(optimal_food)

        if a == 0:
            a=0.7
        b=max(optimal_food)

        for g in ghost:
            optimal_ghost.append(manhattanDistance(newPos,g))
            if manhattanDistance(newPos,g) == 0:
                return -1.0
            elif manhattanDistance(newPos,g)>0 and manhattanDistance(newPos,g)<=1:
                return -1.0/(min(optimal_ghost))

        return 1.0/(a) + 2*max(newScaredTimes)


        #return successorGameState.getScore()

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

    def __init__(self,evalFn = 'scoreEvaluationFunction',depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
    """
    Some extra functions defined that are used by all the questions
    """
    def terminate(self,gameState,depth):
        if depth == self.depth:
            return True
        if gameState.isWin() or gameState.isLose():
            return True
        else:
            return False
    def check_turn(self,player,max_player):
        if player > max_player-1:
            return True
        else:
            return False

    def max_action(self,dict,k):
        if k == 'max':
            return max(dict.iteritems(), key=lambda x: x[1])
        else:
            return min(dict.iteritems(), key=lambda x: x[1])

    def optimal_action(self,action_pair):
        return action_pair[0]

    def probability(self,action):
        p=[]
        for _ in action:
            p.append(random.random())
        sum_p = sum(p)
        p = [i / sum_p for i in p]
        return p

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
        pacman=0
        max_player = gameState.getNumAgents()
        best_min=10000
        best_max=-10000

        def max_node(gameState,depth,player,action):
            if self.terminate(gameState,depth):
                return [action,self.evaluationFunction(gameState)]
            dict={}
            best_possible_value=best_max
            best_possible_action = "None"
            dict[best_possible_action]=best_possible_value
            best=[best_possible_action,best_possible_value]
            action_set=gameState.getLegalActions(player)
            for pos_act in action_set:
                suc=gameState.generateSuccessor(player, pos_act)
                value=min_node(suc,depth,1,pos_act)
                best_possible_value = value[1]
                best_possible_action = pos_act
                dict.update({best_possible_action:best_possible_value})
            key, value = self.max_action(dict,'max')
            return [key,value]
        '''
        --------------------------------------------------------------
        '''
        def min_node(gameState,depth,player,action):
            if self.terminate(gameState,depth):
                return [action,self.evaluationFunction(gameState)]
            if self.check_turn(player,max_player):
                depth = depth + 1
                return max_node(gameState, depth, 0, action)
            dict={}
            best_possible_value = best_min
            best_possible_action = "None"
            dict[best_possible_action] = best_possible_value
            best=[best_possible_action,best_possible_value]
            action_set=gameState.getLegalActions(player)

            for pos_act in action_set:
                suc = gameState.generateSuccessor(player, pos_act)
                value= min_node(suc,depth,player+1,pos_act)
                print value
                best_possible_value=value[1]
                best_possible_action = pos_act
                dict.update({best_possible_action:best_possible_value})
            key, value = self.max_action(dict,'min')
            return [key,value]

        '''
        --------------------------------------------------------------
        '''
        return self.optimal_action(max_node(gameState,0,0,"None"))



        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """




    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacman=0
        max_player = gameState.getNumAgents()
        best_min=10000
        best_max=-10000
        alpha=-10000
        beta=10000


        leaf={}

        def max_node(gameState,depth,player,action,alpha,beta):
            if self.terminate(gameState,depth):
                return [action,self.evaluationFunction(gameState)]
            dict={}
            best_possible_value=best_max
            best_possible_action = "None"
            dict[best_possible_action]=best_possible_value
            action_set=gameState.getLegalActions(player)
            for pos_act in action_set:
                suc=gameState.generateSuccessor(player, pos_act)
                value=min_node(suc,depth,1,pos_act,alpha,beta)
                if value[1]>beta:
                    #print "value max: ",value
                    return value
                alpha = max(alpha, value[1])
                best_possible_value = value[1]
                best_possible_action = pos_act
                dict.update({best_possible_action:best_possible_value})
            key, value = self.max_action(dict,'max')
            return [key,value]
        '''
        --------------------------------------------------------------
        '''
        def min_node(gameState,depth,player,action,alpha,beta):
            if self.terminate(gameState,depth):
                return [action,self.evaluationFunction(gameState)]
            if self.check_turn(player,max_player):
                depth = depth + 1
                return max_node(gameState, depth, 0, action,alpha,beta)
            dict={}
            best_possible_value = best_min
            best_possible_action = "None"
            dict[best_possible_action] = best_possible_value
            best=[best_possible_action,best_possible_value]
            action_set=gameState.getLegalActions(player)
            for pos_act in action_set:
                suc=gameState.generateSuccessor(player, pos_act)
                value=min_node(suc,depth,player+1,pos_act,alpha,beta)
                if value[1]<alpha:
                    return value
                beta = min(beta, value[1])
                best_possible_value=value[1]
                best_possible_action = pos_act
                dict.update({best_possible_action:best_possible_value})
            key, value = self.max_action(dict,'min')
            return [key,value]
        '''
        --------------------------------------------------------------
        '''
        return self.optimal_action(max_node(gameState, 0, 0, "None",-10000,10000))

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
        pacman = 0
        max_player = gameState.getNumAgents()
        best_min = 10000
        best_max = -10000

        leaf = {}

        def max_node(gameState, depth, player,action):
            if self.terminate(gameState,depth):
                return [action,self.evaluationFunction(gameState)]
            dict = {}
            best_possible_value = best_max
            best_possible_action = "None"
            dict[best_possible_action] = best_possible_value
            best = [best_possible_action, best_possible_value]
            action_set = gameState.getLegalActions(player)
            for pos_act in action_set:
                suc = gameState.generateSuccessor(player, pos_act)
                value = min_node(suc, depth, 1, pos_act)
                best_possible_value = value[1]
                best_possible_action = pos_act
                dict.update({best_possible_action: best_possible_value})
            key, value = self.max_action(dict,'max')
            return [key, value]

        '''
        --------------------------------------------------------------
        '''

        def min_node(gameState, depth, player,action):
            if self.terminate(gameState,depth):
                return [action,self.evaluationFunction(gameState)]
            if self.check_turn(player,max_player):
                depth = depth + 1
                return max_node(gameState, depth, 0, action)
            dict = {}
            action_set = gameState.getLegalActions(player)
            ex_max = 0.0
            prob=self.probability(action_set)
            for count,pos_act in enumerate(action_set,start=0):
                suc = gameState.generateSuccessor(player, pos_act)
                value = min_node(suc, depth, player + 1, pos_act)
                print value
                best_possible_value = value[1]
                ex_max+=prob[count]*best_possible_value
                print best_possible_value
                best_possible_action = pos_act
                dict.update({best_possible_action: ex_max})
            return ["None", ex_max]
        '''
        --------------------------------------------------------------
        '''
        return self.optimal_action(max_node(gameState, 0, 0, "None"))
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    foods = currentGameState.getFood()
    newGhostStates=currentGameState.getGhostStates()
    newPos = currentGameState.getPacmanPosition()
    print 'New position:', newPos
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]



    optimal_food = []
    optimal_ghost = []
    food = currentGameState.getFood().asList()

    for f in food:
        optimal_food.append(manhattanDistance(newPos, f))
    if len(optimal_food) == 0:
        return 0
    a = min(optimal_food)

    if a == 0:
        a = currentGameState.getScore()
    cap=[]
    b = max(optimal_food)
    f=currentGameState.getNumFood()

    # for g in currentGameState.getGhostPositions():
    #     optimal_ghost.append(manhattanDistance(newPos, g))
    #     if manhattanDistance(newPos, g) == 0:
    #         return -100000.0
    #     elif manhattanDistance(newPos, g) > 0.0 and manhattanDistance(newPos, g) <= 1.0:
    #         return -100000.0/6

    ghost_PM_dist = []
    ghost_dist_nearest = 0
    for ghost in newGhostStates:
        Ghost_Pos = ghost.getPosition()
        GP_dist = manhattanDistance(Ghost_Pos, newPos)
        ghost_PM_dist.append(GP_dist)

    if len(ghost_PM_dist) > 0:
        ghost_dist_nearest = min(ghost_PM_dist)
    else:
        ghost_dist_nearest = currentGameState.getScore()
        # print ghost_dist_nearest
    ghost_feature = 1 / (ghost_dist_nearest + 1)
    score = 0
    # c=currentGameState.getCapsules()
    # print 'cap',c
    # for i in c:
    #     cap.append(manhattanDistance(newPos,i))
    # if len(optimal_ghost) > 0:
    #     ghost_dist_nearest = min(optimal_ghost)
    # else:
    #     ghost_dist_nearest = currentGameState.getScore()
    #     # print ghost_dist_nearest
    # ghost_feature = 1 / (ghost_dist_nearest + 1)
    # score = 0
    # score=0
    # if currentGameState.isWin():
    #     score = 1000000
    return currentGameState.getScore() + 1.0/(a) +100*score+ 2*(ghost_feature)

    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction





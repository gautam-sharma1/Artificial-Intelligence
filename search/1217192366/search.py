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
from util import Stack
from util import Queue
from util import PriorityQueue
from util import PriorityQueueWithFunction


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
    "*** YOUR CODE HERE ***"
    nodes=Stack()
    fringe=[]
    explored=set()
    visited=[]
    path=[]
    dict={}
    node_start=problem.getStartState()
    if node_start is None:
        return
    if problem.isGoalState(node_start):
        return 'already in the goal position'


    else:
        nodes.push((node_start,path))
        fringe.append(node_start)
        while(nodes):
            curr,path=nodes.pop()
            fringe.remove(curr)
            visited.append(curr)
            explored.add(curr)
            if problem.isGoalState(curr):
                return path
            else:
                next=problem.getSuccessors(curr)
                for states in next:
                    if states[0] not in explored:
                        dict[states[0]]=str(node_start)+'->'+str(path)+'->'+str(states[0])
                        fringe.append(states[0])
                        nodes.push((states[0],path+[states[1]]))
    #print dict[states[0]]

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"


    test=problem.getStartState()

    if type(test[0]) is tuple:


        nodes = Queue()
        dict={}
        fringe=[]
        path = []
        visited = []
        dummy=[]
        start_node = problem.getStartState()

        if problem.isGoalState(start_node):
            return 'already in goal'
        else:
            nodes.push((start_node, path))


            while (nodes):
                curr, path = nodes.pop()


                visited.append(curr)
                if problem.isGoalState(curr):
                    return path
                else:
                    next = problem.getSuccessors(curr)
                    for node in nodes.list:
                        fringe.append(node[0])

                    for states in next:
                        if states[0] not in visited and states[0] not in fringe:
                            nodes.push((states[0], path + [states[1]]))
                            visited.append(states[0])
    else:
            nodes = Queue()
            dict = {}
            fringe = []
            path = []
            visited = []
            dummy = []
            start_node = problem.getStartState()

            if problem.isGoalState(start_node):
                return 'already in goal'
            else:
                nodes.push((start_node, path))

                while (nodes):
                    curr, path = nodes.pop()
                    visited.append(curr)
                    if problem.isGoalState(curr):
                        return path
                    else:
                        next = problem.getSuccessors(curr)
                        for node in nodes.list:
                            fringe.append(node[0])
                        for e in list(visited):
                            dummy.append(e)
                        explored=set(dummy)
                        for states in next:
                            if states[0] not in explored:
                                nodes.push((states[0], path + [states[1]]))
                                visited.append(states[0])

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    nodes = PriorityQueue()
    fringe = []
    path = []
    explored=set([])
    priority=0
    dict={}
    start_node = problem.getStartState()
    if problem.isGoalState(start_node):
        return 'already in goal'
    else:
        nodes.push((start_node, path),priority)
        dict[start_node] = 0
        explored.add(start_node)
        while (nodes):
            curr, path = nodes.pop()

            if problem.isGoalState(curr):
                return path
            else:
                next = problem.getSuccessors(curr)
                for node in nodes.heap:
                    fringe.append(node[0])
                for states in next:
                        if states[0] not in (key for key in dict):
                            cost=problem.getCostOfActions(path + [states[1]])
                            nodes.push((states[0], path + [states[1]]),cost)
                            dict[states[0]]=cost
                            explored.add(states[0])
                        elif states[0] in (key for key in dict) and (problem.getCostOfActions(path + [states[1]]) < dict[states[0]]) :
                            cost = problem.getCostOfActions(path + [states[1]])
                            nodes.push((states[0], path + [states[1]]), cost)
                            dict[states[0]] = cost
                            explored.add(states[0])


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    #"""Search the node that has the lowest combined cost and heuristic first."""
    #"*** YOUR CODE HERE ***"



    heu=heuristic

    test = problem.getStartState()
    if type(test[0]) is not tuple:
        nodes = PriorityQueue()
        fringe = []
        path = []
        explored = set()
        priority = 0
        dict = {}
        start_node = problem.getStartState()
        if problem.isGoalState(problem.getStartState()):
            return
        nodes.push((problem.getStartState(), path), priority)
        explored.add(start_node)
        dict[start_node] = 0
        while not nodes.isEmpty():
            curr, path = nodes.pop()
            if problem.isGoalState(curr):
                return path
            else:
                next = problem.getSuccessors(curr)
                for node in nodes.heap:
                    fringe.append(node[0])
                for states in next:
                    if states[0] not in (key for key in dict):
                        h = heu(states[0],problem)
                        updated_path = path + [states[1]]
                        cost = problem.getCostOfActions(updated_path)+h
                        nodes.push((states[0], updated_path), cost)
                        dict[states[0]] = cost
                        explored.add(states[0])
                    elif states[0] in (key for key in dict) and (problem.getCostOfActions(path + [states[1]])+heu(states[0],problem) < dict[states[0]]):
                        h = heu(states[0],problem)
                        updated_path = path + [states[1]]
                        cost = problem.getCostOfActions(updated_path)+h
                        nodes.update((states[0], updated_path), cost)
                        dict[states[0]] = cost
                        explored.add(states[0])
    else:
        nodes = PriorityQueue()
        fringe = []
        path = []
        explored = set()
        visited=[]
        priority = 0
        dict = {}
        cost=0
        start_node = problem.getStartState()

        if problem.isGoalState(problem.getStartState()):
            return
        nodes.push((start_node, path),priority)
        fringe.append(start_node[0])
        dict[start_node[0]] = 0
        while (nodes) :
            curr, path = nodes.pop()

            if problem.isGoalState(curr):
                return path
            if curr not in visited:
                visited.append(curr)
                next = problem.getSuccessors(curr)
                for states,c_path,c in next:
                    if states[0] in (key for key in dict):
                        h=heu(states,problem)
                        updated_path=path+[c_path]
                        cost=h+problem.getCostOfActions(updated_path)+c
                        nodes.update((states,updated_path),cost)
                    else:
                        updated_path = path + [c_path]
                        dict[states[0]]= problem.getCostOfActions(updated_path)
                        h = heu(states, problem)
                        cost = dict[states[0]]
                        cost=cost+h
                        nodes.push((states, updated_path), cost)






bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

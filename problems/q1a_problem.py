import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1a_problem:
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.gameState: GameState = gameState
        self.layout_width = self.gameState.data.layout.width
        self.layout_height = self.gameState.data.layout.height
        self.goal = gameState.getFood().asList()[0]

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.gameState.getPacmanPosition()


    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        # if state.getPacmanPosition() == self.goal:
        if state == self.goal:
            return True
        else:
            return False

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the successors they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        # ------------------------------------------
        "*** YOUR CODE HERE ***"
        successors = []
        x, y = state # State represents a position (x, y)
        
        if y > 0:  
            if not self.gameState.hasWall(x, y-1): # Can move north
                successors.append(((x, y-1), 'South', 1))
        if x < self.layout_width - 1:  
            if not self.gameState.hasWall(x+1, y): # Can move east
                successors.append(((x+1, y), 'East', 1))
        if y < self.layout_height - 1:  
            if not self.gameState.hasWall(x, y+1): # Can move south
                successors.append(((x, y+1), 'North', 1))
        if x > 0:  
            if not self.gameState.hasWall(x-1, y): # Can move west
                successors.append(((x-1, y), 'West', 1))
    
        successors.append(((x, y), 'Stop', 0))
            
        return successors



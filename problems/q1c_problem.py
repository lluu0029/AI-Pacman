import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
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
        self.startingGameState: GameState = gameState
        self.goals = self.startingGameState.getFood().asList()

        self.layout_width = self.startingGameState.data.layout.width
        self.layout_height = self.startingGameState.data.layout.height

        for w in range(self.layout_width):
            for h in range(self.layout_height):
                if self.startingGameState.hasFood(w, h):
                    self.goals.append((w, h))

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.startingGameState

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        if state.getNumFood() == 0:
            return True
        else:
            return False 

    @log_function
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
        "*** YOUR CODE HERE ***"
        successors = []
        
        for action in state.getLegalActions():
            successors.append((state.generatePacmanSuccessor(action), action, 1))
            
        return successors


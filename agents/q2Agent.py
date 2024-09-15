import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


def scoreEvaluationFunction(gameState, prev_positions):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    score = gameState.getScore()
    pacman_position = gameState.getPacmanPosition()
    food_list = gameState.getFood().asList()
    ghost_states = gameState.getGhostStates()
    ghost_positions = gameState.getGhostPositions()
    capsule_list = gameState.getCapsules()

    min_food_dist = float('inf')
    min_ghost_dist = float('inf')
    min_capsule_dist = float('inf')
    min_ghost_state = None
    min_ghost_position = None

    if len(food_list) == 0: # In the given game state, pacman has eaten the final food, thus game is won.
        return float('inf')
    # Calculate distance to the nearest food
    for food_position in food_list:
        distance = manhattanDistance(pacman_position, food_position)
        if distance < min_food_dist:
            min_food_dist = distance

    ghost_distances = []
    # Calculate distance to the nearest ghost
    for ghost_state in ghost_states:
        ghost_position = ghost_state.getPosition()
        distance = manhattanDistance(pacman_position, ghost_position)
        ghost_distances.append(distance)
        if distance < min_ghost_dist:
            min_ghost_dist = distance
            min_ghost_state = ghost_state
            min_ghost_position = ghost_position

    # Calculate distance to the nearest capsule
    for capsule_position in capsule_list:
        distance = manhattanDistance(pacman_position, capsule_position)
        if distance < min_capsule_dist:
            min_capsule_dist = distance

    # score = 0

    legal_actions = gameState.getLegalPacmanActions()

    if len(legal_actions) <= 2:
        score -= 10*len(food_list)

    if len(legal_actions) == 1:
        score -= 150

    if min_ghost_dist == 0:
        return float('-inf')

    # Factor in nearest food, scaled by remaining food factor
    score += 10.0 / (min_food_dist+1)
    score -= 5.0 * len(food_list)  # Penalize for each remaining food pellet

    # If the closest ghost is 2 or less positions away, heavily reduce score.

    # Factor in remaining food, pacman will want to reduce the number of food.
    # score -= 10.0 * (len(food_list) + 1)
    
    # Penalties / incentives for the nearest ghost.
    if min_ghost_state.scaredTimer > 0: # If the closest ghost is scared, add incentive.
        score += 200.0 / (min_ghost_dist + 1)
    else: 
        if len(capsule_list) != 0: # Incentive to reach nearest capsule if the nearest ghost is not scared.
            score += 30 / (min_capsule_dist + 1)
        if min_ghost_dist <= 2.5: # Heavy penalty if the nearest ghost is 2 or less positions away.
            score -= 1000 / (min_ghost_dist + 1)
        if len(capsule_list) != 0 and min_capsule_dist < min_ghost_dist: # Reducing penalty for being near ghosts if a capsule is near as well.
            score -= 10.0 / (min_ghost_dist + 1)
        elif min_ghost_dist <= 5.5: # Reduce score if the nearest ghost is 5 or less positions away.
            score -= 30.0 / (min_ghost_dist + 1)

    # Penalising if pacman gets stuck in a loop.
    # print(prev_positions)
    if len(prev_positions) == 5:
        if prev_positions[1] == prev_positions[3]:
            if pacman_position == prev_positions[0] and pacman_position == prev_positions[2] and pacman_position == prev_positions[4]:
                score -= 500

    # print(int(score), min_food_dist, min_ghost_dist)
    return score

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.prev_positions = []

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghost_positions are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"
        prev_positions = self.prev_positions

        score, action = alphabeta(gameState, self.depth, float('-inf'), float('inf'), 0, prev_positions)

        if action is None:
            action = 'Stop'

        if len(prev_positions) != 5:
            prev_positions.append(gameState.generatePacmanSuccessor(action).getPacmanPosition())
        else:
            prev_1_to_4 = prev_positions[1:]
            self.prev_positions = prev_1_to_4
            self.prev_positions.append(gameState.generatePacmanSuccessor(action).getPacmanPosition())

        # print('Chosen score: ', score, action, '\n')

        
        # self.prev_positions.append(gameState.generatePacmanSuccessor(action).getPacmanPosition())

        return action

        
def alphabeta(gameState, depth, alpha, beta, agent, prev_positions):
    num_agents = gameState.getNumAgents() - 1

    if depth == 0 or gameState.isWin() or gameState.isLose():
        return scoreEvaluationFunction(gameState, prev_positions), None
        
    if agent == 0: # Maximise score for the Pacman
        best_score = float('-inf')
        best_action = None
        for action in gameState.getLegalPacmanActions():
            successor_state = gameState.generatePacmanSuccessor(action)
            successor_score, _ = alphabeta(successor_state, depth - 1, alpha, beta, 1, prev_positions) # 1 represents the first ghost.
            if successor_score > best_score:
                best_score = successor_score
                best_action = action
            alpha = max(alpha, successor_score)
            if beta <= alpha:
                break
        return best_score, best_action
    else: # Minimise score for the ghost
        best_score = float('inf')
        best_action = None
        for action in gameState.getLegalActions(agent):
            successor_state = gameState.generateSuccessor(agent, action)
            next_agent = (agent + 1) % (num_agents+1)
            if next_agent == 0:
                next_depth = depth - 1
            else:
                next_depth = depth
            successor_score, _ = alphabeta(successor_state, next_depth, alpha, beta, next_agent, prev_positions)
            if successor_score < best_score:
                best_score = successor_score
                best_action = action
            beta = min(beta, successor_score)
            if beta <= alpha:
                break
        return best_score, best_action
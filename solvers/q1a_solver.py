#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

def q1a_solver(problem: q1a_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        self.pq = util.PriorityQueue()
        self.prev_actions = {}
        self.g_score = {}
        self.current_position = None


def astar_initialise(problem: q1a_problem):
    # YOUR CODE HERE
    astarData = AStarData()

    # Pushing starting position, and heuristic of starting position.
    astarData.pq.push(problem.getStartState(), astar_heuristic(problem.getStartState(), problem.goal))
    # Setting path cost to the starting position to be 0.
    astarData.g_score[problem.getStartState()] = 0

    return astarData

def astar_loop_body(problem: q1a_problem, astarData: AStarData):
    # No more nodes to be expanded.
    if astarData.pq.isEmpty():
        return True, []

    # Popping current position.
    astarData.current_position = astarData.pq.pop()

    if problem.isGoalState(astarData.current_position): # Goal is reached
        path = []
        while astarData.current_position != problem.getStartState(): # Reconstructing path
            astarData.current_position, action = astarData.prev_actions[astarData.current_position]
            path.append(action)
        path.reverse()
        return True, path

    for successor_position, action, cost in problem.getSuccessors(astarData.current_position): # For each possible successor based on legal moves.
        successor_g_score = cost + astarData.g_score[astarData.current_position] # Cost of travelling to the successor position + cost to travel to current position.

        # If successor position not in g_score, no path to it has been found yet, thus update.
        # If successor_g_score is less than what is currently stored, a shorter path has been found, thus update.
        if successor_position not in astarData.g_score or successor_g_score < astarData.g_score[successor_position]: 
            # Updating scores.
            astarData.g_score[successor_position] = successor_g_score 
            f_score = astar_heuristic(successor_position, problem.goal) + successor_g_score
            astarData.pq.push(successor_position, f_score)
            astarData.prev_actions[successor_position] = (astarData.current_position, action)

    return False, None # Search algorithm still in progress

# Manhattan distance heuristic
def astar_heuristic(current, goal):
    # YOUR CODE HERE
    x1, y1 = current
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
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

import heapq

class PriorityQueueTieBreaker:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority, h_score):
        entry = (priority, h_score, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority, h_cost):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, g, c, i) in enumerate(self.heap):
            if i == item:
                if p < priority or (p == priority and g <= h_cost):
                    break
                del self.heap[index]
                self.heap.append((priority, h_cost, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority, h_cost)

class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        # self.pq = util.PriorityQueue()
        self.pq = PriorityQueueTieBreaker()
        self.prev_actions = {}
        self.g_score = {}
        self.current_position = None

def astar_initialise(problem: q1b_problem):
    # YOUR CODE HERE
    astarData = AStarData()

    # Pushing item (start position), priority (heuristic from start position). 
    astarData.pq.push(problem.getStartState(), astar_heuristic(problem.getStartState(), problem.goals), astar_heuristic(problem.getStartState(), problem.goals))
    # Setting path cost to start position = 0
    astarData.g_score[problem.getStartState()] = 0

    return astarData

def astar_loop_body(problem: q1b_problem, astarData: AStarData):
    # YOUR CODE HERE
    if astarData.pq.isEmpty():
        return True, []

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
            astarData.g_score[successor_position] = successor_g_score
            f_score = astar_heuristic(successor_position, problem.goals) + successor_g_score
            astarData.pq.push(successor_position, f_score, astar_heuristic(successor_position, problem.goals))
            astarData.prev_actions[successor_position] = (astarData.current_position, action)

    return False, None # Search algorithm still in progress

# Manhattan distance heuristic to the nearest goal.
def astar_heuristic(current, goals):
    # YOUR CODE HERE
    x1, y1 = current
    h_scores = []

    for goal in goals: # Calculates heuristic scores for all goals.
        x2, y2 = goal
        h_scores.append(abs(x1 - x2) + abs(y1 - y2))

    return min(h_scores) # Returns the lowest heuristic score, representing the lowest estimate goal.


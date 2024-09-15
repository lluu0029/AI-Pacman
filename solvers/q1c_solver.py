#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    # YOUR CODE HERE
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

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
        self.current_game_state = None # Current game state being explored by the A* algorithm.
        self.food_remaining = None

def astar_initialise(problem: q1c_problem):
    # YOUR CODE HERE
    astarData = AStarData()

    # Pushing item (start position, path), priority (heuristic from start position). 
    astarData.pq.push((problem.getStartState(), []), astar_heuristic(problem.getStartState().getPacmanPosition(), problem.goals), astar_heuristic(problem.getStartState().getPacmanPosition(), problem.goals))
    # Setting path cost to start position = 0
    astarData.g_score[(problem.getStartState().getPacmanPosition(), problem.getStartState().getNumFood())] = 0

    return astarData

def astar_loop_body(problem: q1c_problem, astarData: AStarData):
    # YOUR CODE HERE
    if astarData.pq.isEmpty():
        return True, []

    astarData.current_game_state, path = astarData.pq.pop()
    current_position = astarData.current_game_state.getPacmanPosition()
    current_numFood = astarData.current_game_state.getNumFood()

    # print(astarData.current_game_state.getPacmanPosition(), astarData.current_game_state.getNumFood())
    if problem.isGoalState(astarData.current_game_state):
        return True, path

    for successor, action, cost in problem.getSuccessors(astarData.current_game_state):
        successor_g_score = astarData.g_score[(current_position, current_numFood)] + cost
        successor_position = successor.getPacmanPosition()
        successor_num_food = successor.getNumFood()

        if (successor_position, successor_num_food) not in astarData.g_score or successor_g_score < astarData.g_score[(successor_position, successor_num_food)]:
            new_path = path + [action]
            successor_position = successor.getPacmanPosition()
            astarData.g_score[(successor_position, successor_num_food)] = successor_g_score
            astarData.pq.push((successor, new_path), astar_heuristic(successor_position, successor.getFood().asList()) + successor_g_score, astar_heuristic(successor_position, successor.getFood().asList()))
    
    return False, None


# Factors in the closest goal, sum of the distances to the goals, and the number of goals.
def astar_heuristic(current, goals):
    # YOUR CODE HERE
    x1, y1 = current

    distances = []
    for goal in goals:
        x2, y2 = goal
        distances.append(abs(x1 - x2) + abs(y1 - y2))

    if len(distances) == 0:
        return 0

    return (min(distances) + sum(distances)*0.001 + len(goals)*10)

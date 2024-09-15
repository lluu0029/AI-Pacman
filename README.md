# Assignment 1: AI Pacman

## Q1 Single Agent Search
### Q1a Shortest path to a single food dot
Pacman finds the optimal path to the single food dot in a layout.
This solution makes use of the A* algorithm using a Manhattan distance heuristic.
- **Running all layouts using Windows:**
  ```./q1a.bat```
- **Using command line for a chosen layout:**
```bash
python pacman.py -l layouts/q1a_tinyMaze.lay -p SearchAgent -a fn=q1a_solver,prob=q1a_problem --timeout=1
```

### Q1b Shortest path to the nearest food dot
Pacman finds the optimal path to the nearest food dot when there are multiple in a layout.
This solution makes use of the A* algorithm, with a heuristic taking into account the nearest food dot.
- **Running all layouts using Windows:**
  './q1b.bat'
- **Using command line for a chosen layout:**
  'python pacman.py -l layouts/q1b_tinyCorners.lay -p SearchAgent -a fn=q1b_solver,prob=q1b_problem --timeout=5'

### Q1c Shortest path to reach all food dots
Pacman finds the optimal path to eat all the food dots in a layout.
This solution makes use of the A* algorithm, with a weighted heuristic taking into account the distance to the closest goal, sum of distances to all remaining food dots and the number of remaining food dots.
- **Running all layouts using Windows:**
  './q1c.bat'
- **Using command line for a chosen layout:**
  'python pacman.py -l layouts/q1c_tinySearch.lay -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10'

## Q2 Adversarial Search
Pacman controller which plays the game with multiple food dots and ghosts, attempting to maximise the score.
This solution makes use of the alpha-beta algorithm, performing an adversarial search in each game state, with Pacman as the maximiser agent and Ghosts as the minimiser agents.
- **Running all layouts using Windows:**
  './q2.bat'
- **Using command line for a chosen layout:**
  'python pacman.py -l layouts/q2_testClassic.lay -p Q2_Agent --timeout=30'


This repository is originally cloned from the `assignment1` branch of the repository at <https://github.com/ethantwills/fit3080_2024>. If there are updates to this code, please merge from here.

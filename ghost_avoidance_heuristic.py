import math
import search

class GhostAvoidanceHeuristic(search.Problem):
    
    def __init__(self, maze, initial_state, goal_state, food_tile_cost=1, empty_tile_cost=1, ghost_proximity_range=10, ghost_proximity_cost=20):
        super().__init__(initial_state, goal_state)
        self.maze = maze
        self.food_tile_cost = food_tile_cost
        self.empty_tile_cost = empty_tile_cost
        self.ghost_proximity_range = ghost_proximity_range
        self.ghost_proximity_cost = ghost_proximity_cost
        

    def h(self, node):
        """
        It takes into consideration the straight-line distance from a node's state to the goal, and also the proximity to the ghosts in the maze
        """
        x1, y1 = node.state
        x2, y2 = self.goal

        goal_dist = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))

        ghost_proximity = 0

        for ghost in self.maze.get_ghost():
            xg, yg = ghost
            ghost_dist = math.sqrt(((xg - x1)**2) + ((yg - y1)**2))
            if ghost_dist <= self.ghost_proximity_range:
                ghost_proximity += self.ghost_proximity_cost/ghost_dist

        return goal_dist + ghost_proximity


import enviroment
import search
from enum import Enum

class Actions(Enum):
	RIGHT = [0, 1]
	LEFT = [0, -1]
	UP = [1, 0]
	DOWN = [-1, 0]

class Problem(search.Problem):

	def __init__(self, maze, initial_state, goal_state):
		self.maze = maze
		super().__init__(initial_state, goal_state)

	def actions(self, state):
		"""Return the actions that can be executed in the given
		state. The result would typically be a list, but if there are
		many actions, consider yielding them one at a time in an
		iterator, rather than building them all at once."""
		return [action for action in Actions if self.maze.isValidPosition(self.result(state, action))]

	def result(self, state, action):
		"""Return the state that results from executing the given
		action in the given state. The action must be one of
		self.actions(state)."""
		return [x + y for x, y in zip(state, action.value)]

# if __name__ == "__main__":
# 	maze, initial_state, goal_state = enviroment.getMazeTest()
# 	problem = Problem(maze, initial_state, goal_state)

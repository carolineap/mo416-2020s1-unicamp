import sys
import numpy as np
from enum import Enum
from enviroment import Maze, Position


class Actions(Enum):
	UP = (1, 0)
	DOWN = (-1, 0)
	RIGHT = (0, 1)
	LEFT = (0, -1)


class ShockWaveMaze(Maze):

	def __init__(self, num_rows, num_cols):
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.transversable_positions = []
		self.ghost_positions = []

		self.grid = []

	def get_transversable(self):
		return [tp.position for tp in self.transversable_positions]

	def get_food(self):
		return [tp.position for tp in self.transversable_positions if tp.food]
	
	def is_food(self, position):
		ret = position in self.get_food()
		return ret

	def get_ghost(self):
		return [g.position for g in self.ghost_positions]

	def is_allowed(self, position):
		return position[0] >= 0 and position[0] < self.num_rows and position[1] >= 0 and position[1] < self.num_cols and position in self.get_transversable()
	
	def is_in_boundary(self, position):
		return position[0] >= 0 and position[0] < self.num_rows and position[1] >= 0 and position[1] < self.num_cols

	def get_int_grid(self, initial_position, goal_position):
		#this method is necessary only for plots
		grid = []
		for i in range(0, self.num_rows):
			row = []
			for j in range(0, self.num_cols):
				if (i, j) == initial_position:
					row.append(0)
				elif (i, j) == goal_position:
					row.append(1)
				elif (i, j) in self.get_transversable() and not (i, j) in self.get_food():
					row.append(2)
				elif (i, j) in self.get_food():
					row.append(3)
				elif (i, j) in self.get_ghost():
					row.append(4)
				else:
					row.append(5)

			grid.append(row)
		return grid

	def get_final_grid(self, initial_position, goal_position, path):
		#this method is necessary only for plots
		grid = []
		for i in range(0, self.num_rows):
			row = []
			for j in range(0, self.num_cols):
				if (i, j) == initial_position:
					row.append(0)
				elif (i, j) == goal_position:
					row.append(1)
				elif (i, j) in path:
					if (i, j) in self.get_food():
						row.append(4)
					else:
						row.append(2)
				else:
					row.append(3)
				
			grid.append(row)

		return grid
	
	def elem_wise_sum(self, a, b):
		return tuple(map(sum, zip(a, b)))
	
	def set_shockwave(self, goal_position):
		grid = np.empty([self.num_cols, self.num_rows], dtype=int)
		grid.fill(-1) 
		grid[goal_position[0]][goal_position[1]] = 0

		queue = [goal_position]		
		while len(queue) > 0:
			i, j = queue[0]
			for action in Actions:
				neighbor = self.elem_wise_sum(queue[0], action.value)

				if (self.is_allowed(neighbor) and grid[neighbor[0]][neighbor[1]] == -1):
					queue.append(neighbor)
					grid[neighbor[0]][neighbor[1]] = grid[i][j] + 1
		
			queue.pop(0)
		
		self.grid = grid


def read_maze(maze_file, num_rows, num_cols):
	maze = ShockWaveMaze(num_rows, num_cols)
	initial_position = goal_position = (-1, -1)
		
	k = 0
	for i in range(0, maze.num_rows):
		for j in range(0, maze.num_cols):
			pos = maze_file[k]
			
			position = Position((i, j))
			
			if pos == 'o':
				maze.ghost_positions.append(position)
			elif pos != '|':
				if pos == '.':
					position.food = True
				elif pos == 'p':
					initial_position = (i, j)
				elif pos == 'g':
					goal_position = (i,j)

				maze.transversable_positions.append(position)
			
			k += 1
		k+=1
	
	maze.set_shockwave(goal_position)
	return maze, initial_position, goal_position

def getMazeTest():
	maze_file = open("maze-test.txt","r").read()
	return read_maze(maze_file, num_rows = 28, num_cols = 28)


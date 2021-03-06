import sys
import yaml
import numpy as np
from src.actions import Actions


class Position:

	def __init__(self, position, food=False):
		self.position = position
		self.food = food


class Maze:

	def __init__(self, num_rows, num_cols):
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.transversable_positions = []
		self.ghost_positions = []

		self.shockwave_grid = []

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
				elif (i, j) in self.get_transversable():
					row.append(2)
				elif (i, j) in self.get_ghost():
					row.append(3)
				else:
					row.append(4)
			grid.append(row)

		food_x = []
		food_y = []

		for i, j in self.get_food():
			if ((i, j) != initial_position and (i, j) != goal_position):
				food_x.append(i)
				food_y.append(j)

		return grid, food_x, food_y 

	def get_final_grid(self, initial_position, goal_position, path):
		#this method is necessary only for plots
		grid = []
		food_x = []
		food_y = []

		for i in range(0, self.num_rows):
			row = []
			for j in range(0, self.num_cols):
				if (i, j) == initial_position:
					row.append(1)
				elif (i, j) == goal_position:
					row.append(2)
				elif (i, j) in path:
					row.append(3)
					if (i, j) in self.get_food():
						food_x.append(i)
						food_y.append(j)
				else:
					row.append(4)
				
			grid.append(row)

		return grid, food_x, food_y


class ShockWaveMaze(Maze):
	def __init__(self, num_rows, num_cols):
		super().__init__(num_rows, num_cols)
		self.shockwave_grid = []
	
	def set_shockwave(self, goal_position):
		def elem_wise_sum(a, b):
			return tuple(map(sum, zip(a, b)))
		
		# The goal position must be a valid position, if not
		# generate a 0s grid
		if goal_position == (-1, -1):
			grid = np.zeros([self.num_rows, self.num_cols], dtype=int)
			self.shockwave_grid = grid
			return

		grid = np.empty([self.num_rows, self.num_cols], dtype=int)
		grid.fill(-1) 
		grid[goal_position[0]][goal_position[1]] = 0

		queue = [goal_position]
		while len(queue) > 0:
			i, j = queue[0]
			for action in Actions:
				neighbor = elem_wise_sum(queue[0], action.value)
				
				# Tunnel addition
				neighbor = neighbor[0] % self.num_rows, neighbor[1] % self.num_cols

				if (self.is_allowed(neighbor) and grid[neighbor[0]][neighbor[1]] == -1):
					queue.append(neighbor)
					grid[neighbor[0]][neighbor[1]] = grid[i][j] + 1
		
			queue.pop(0)

		self.shockwave_grid = grid


def set_ghost(ghost_arq, maze):
	ghosts = []
	with open(ghost_arq, "r") as ghost_file:
		data = yaml.load(ghost_file, Loader=yaml.Loader)
		for g in data:
			ghosts.append(Position(tuple(g)))
	
	maze.ghost_positions = ghosts

	maze_pos = [tuple(g.position) for g in maze.transversable_positions]
	
	for ghost in ghosts:
		if ghost.position in maze_pos:
			index = maze_pos.index(ghost.position)

			a = maze.transversable_positions.pop(index)
			b = maze_pos.pop(index)


def read_maze(maze_file, num_rows, num_cols, maze_class=Maze):
	maze = maze_class(num_rows, num_cols)
	initial_position = goal_position = (-1, -1)
		
	k = 0
	for i in range(maze.num_rows - 1, -1, -1):
		for j in range(0, maze.num_cols):
			pos = maze_file[k]
			position = Position((i, j))
			
			if pos == 'o':
				# maze.ghost_positions.append(position)
				maze.transversable_positions.append(position)
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
	
	# If the Maze is the Shockwave Maze, we must set the shockwave grid
	if maze_class == ShockWaveMaze:
		maze.set_shockwave(goal_position)

	return maze, initial_position, goal_position

def getMazeTest(maze_arq, num_rows, num_cols, maze_class=Maze):
	maze_file = open(maze_arq, "r").read()
	return read_maze(maze_file, num_rows, num_cols, maze_class)


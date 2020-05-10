import sys
import numpy as np
from src.actions import Actions


class Position:

	def __init__(self, position, food=False):
		self.position = position
		self.food = food
		self.wavefront_value = -1

class Maze:

	def __init__(self, num_rows, num_cols):
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.transversable_positions = []
		self.ghost_positions = []

	#	self.wavefront_grid = []
	def find_transversable_object(self, position):
		for obj in self.transversable_positions:
			if obj.position == position:
				return obj
		return None

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

	def get_wavefront_grid(self):
		#this method is necessary only for plots
		grid = []
		for i in range(0, self.num_rows):
			row = []
			for j in range(0, self.num_cols):
				position = self.find_transversable_object((i, j))
				if position:
					row.append(position.wavefront_value)
				else:
					row.append(-1)
			grid.append(row)

		return grid

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

	def set_wavefront(self, goal_position):
		
		def elem_wise_sum(a, b):
			return tuple(map(sum, zip(a, b)))
		
		if goal_position not in self.get_transversable():
			return

		position = self.find_transversable_object(goal_position)
		position.wavefront_value = 0

		queue = [position]
		while len(queue) > 0:

			for action in Actions:
				neighbor = elem_wise_sum(queue[0].position, action.value)
				
				neighbor = neighbor[0] % self.num_rows, neighbor[1] % self.num_cols

				if self.is_allowed(neighbor):
					neighbor_obj = self.find_transversable_object(neighbor)
					if neighbor_obj.wavefront_value  == -1:
						queue.append(neighbor_obj)
						neighbor_obj.wavefront_value = queue[0].wavefront_value + 1
		
			queue.pop(0)


def read_maze(maze_file, num_rows, num_cols, maze_class=Maze):
	maze = maze_class(num_rows, num_cols)
	initial_position = goal_position = (-1, -1)
		
	k = 0
	for i in range(maze.num_rows - 1, -1, -1):
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

	return maze, initial_position, goal_position

def getMazeTest(maze_arq, num_rows, num_cols, maze_class=Maze):
	maze_file = open(maze_arq, "r").read()
	return read_maze(maze_file, num_rows, num_cols, maze_class)
import sys

class Position:
	def __init__(self):
		self.isTransversable = True
		self.isWall = False
		self.isGhost = False
		self.isFood = False

class Maze:
	def __init__(self, num_rows, num_cols):
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.grid = [[Position() for j in range(num_cols)] for i in range(num_rows)]

	def isValidPosition(self, position):
		return position[0] >= 0 and position[0] < self.num_rows and position[1] >= 0 and position[1] < self.num_cols and self.grid[position[0]][position[1]].isTransversable


def read_maze(maze, num_rows, num_cols):
	maze = Maze(num_rows, num_cols)
	initial_position = goal_position = [-1, -1]

	k = 0
	for i in range(0, maze.num_rows):
		for j in range(0, maze.num_cols):
			pos = file[k]
			if pos == '|':
				maze.grid[i][j].isWall = True
				maze.grid[i][j].isTransversable = False
			elif pos == '.':
				maze.grid[i][j].isFood = True
			elif pos == 'o':
				maze.grid[i][j].isGhost = True
				maze.grid[i][j].isTransversable = False
			elif pos == 'p':
				initial_position = [i, j]
			elif pos == 'g':
				goal_position = [i, j]
			
			k += 1

	return maze, initial_position, goal_position

def getMazeTest():
	maze = open("maze-test.txt","r").read()
	return read_maze(file, num_rows = 31, num_cols = 29)


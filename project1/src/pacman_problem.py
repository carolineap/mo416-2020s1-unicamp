from collections import deque
import math
import random

# AIMA Libs
from lib.utils import memoize, PriorityQueue
import lib.search

# Pacman files
from src.actions import Actions
from src.pacman_node import Node


class PacmanProblem(lib.search.Problem):

	def __init__(self, maze, initial_state, goal_state, food_tile_cost=1, empty_tile_cost=1000, ghost_proximity_range=10, ghost_proximity_cost=20):
		super().__init__(initial_state, goal_state)

		self.maze = maze

		# Variables for the path cost
		self.food_tile_cost = food_tile_cost
		self.empty_tile_cost = empty_tile_cost

		# Variables for the ghost avoidance heuristic
		self.ghost_proximity_range = ghost_proximity_range
		self.ghost_proximity_cost = ghost_proximity_cost

	def actions(self, state):
		"""Return the actions that can be executed in the given
		state. The result would typically be a list, but if there are
		many actions, consider yielding them one at a time in an
		iterator, rather than building them all at once."""
		return [action for action in Actions if self.maze.is_allowed(self.result(state, action))]

	def result(self, state, action):
		"""Return the state that results from executing the given
		action in the given state. The action must be one of
		self.actions(state)."""
		position = tuple(map(sum, zip(state, action.value)))
		
		if position[0] < 0 or position[0] >= self.maze.num_rows:
			x = position[0]%self.maze.num_rows
		else:
			x = position[0]

		if position[1] < 0 or position[1] >= self.maze.num_cols:
			y = position[1]%self.maze.num_cols
		else:
			y = position[1]

		return (x, y)

	def check_food(self, state):
		return state in self.maze.get_food()

	def h(self, node):
		"""h function is straight-line distance from a node's state to goal."""
		x1, y1 = node.state
		x2, y2 = self.goal
		return abs(x2 - x1) + abs(y2 - y1)
	
	def h_euclidean(self, node):
		x1, y1 = node.state
		x2, y2 = self.goal

		return math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
	
	def h_ghost_avoidance_euclidean(self, node):
		goal_dist = self.h_euclidean(node)

		x1, y1 = node.state
		ghost_proximity = 0

		for ghost in self.maze.get_ghost():
			xg, yg = ghost
			ghost_dist = math.sqrt(((xg - x1)**2) + ((yg - y1)**2))
			if ghost_dist <= self.ghost_proximity_range:
				ghost_proximity += self.ghost_proximity_cost/ghost_dist

		return goal_dist + ghost_proximity
	
	def h_ghost_avoidance_manhattam(self, node):
		goal_dist = self.h(node)

		x1, y1 = node.state
		ghost_proximity = 0

		for ghost in self.maze.get_ghost():
			xg, yg = ghost
			ghost_dist = math.sqrt(((xg - x1)**2) + ((yg - y1)**2))
			if ghost_dist <= self.ghost_proximity_range:
				ghost_proximity += self.ghost_proximity_cost/ghost_dist

		return goal_dist + ghost_proximity
	
	def h_shockwave(self, node):
		"""h function is the shockwave distance to the goal."""
		x1, y1 = node.state
		return self.maze.shockwave_grid[x1][y1]

	def path_cost(self, c, state1, action, state2):
		"""Return the cost of a solution path that arrives at state2 from
		state1 via action, assuming cost c to get up to state1. If the problem
		is such that the path doesn't matter, this function will only look at
		state2. If the path does matter, it will consider c and maybe state1
		and action. The default method costs 1 for every step in the path."""
		if self.maze.is_food(state2):
			return c + self.food_tile_cost
		else:
			return c + self.empty_tile_cost


def depth_first_graph_search(problem):
	expanded_nodes = 0
	food_nodes = 0
	frontier = [(Node(problem.initial))]
	tam = len(frontier)
	
	explored = set()
	while frontier:
		node = frontier.pop()
		expanded_nodes += 1
		food_nodes += problem.check_food(node.state)
		if problem.goal_test(node.state):
			return node, expanded_nodes, food_nodes, tam
		explored.add(node.state)
		frontier.extend(child for child in node.expand(problem)
						if child.state not in explored and child not in frontier)
		new_tam = len(frontier)
		if (new_tam > tam):
			tam = new_tam
	return None, expanded_nodes, food_nodes, tam

def breadth_first_graph_search(problem):
	expanded_nodes = 0
	food_nodes = 0
	node = Node(problem.initial)
	tam = 1
	
	if problem.goal_test(node.state):
		return node
	frontier = deque([node])
	
	explored = set()
	while frontier:
		node = frontier.popleft()
		expanded_nodes += 1
		food_nodes += problem.check_food(node.state)
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				#tam += 1
				if problem.goal_test(child.state):
					return child, expanded_nodes, food_nodes, tam
				frontier.append(child)
		new_tam = len(frontier)
		if (new_tam > tam):
			tam = new_tam
	return None, expanded_nodes, food_nodes, tam

def best_first_graph_search(problem, f, display=False):
	expanded_nodes = 0
	food_nodes = 0
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	tam = 1
	
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
			return node, expanded_nodes, food_nodes, tam
		expanded_nodes += 1
		food_nodes += problem.check_food(node.state)  
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
				#tam += 1
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
			new_tam = len(frontier)
			if (new_tam > tam):
				tam = new_tam
	return None, expanded_nodes, food_nodes, tam

def hill_climbing_search(problem, h=None, display=False):
	"""Hill Climbing search is a local search method that tries to find the best state to search
	according to an objective function (h). If there is no best state to pursue up to this point
	(local min/max), the algorithm stops."""
	expanded_nodes = 0
	food_nodes = 0
	h = memoize(h or problem.h, 'h')
	node = Node(problem.initial)
	finished = False
	explored = set()
	tam = 1

	while not finished:
		if problem.goal_test(node.state):
			if display:
				print("Goal found ", len(explored), " paths have been expanded.")
			return node, expanded_nodes, food_nodes, tam
		expanded_nodes += 1
		food_nodes += problem.check_food(node.state)
		explored.add(node.state)

		next_node = node
		best = []
		for child in node.expand(problem):
			if child.state not in explored:
				if h(child) < h(next_node):
					best.clear()
					next_node = child
					best.append(child)
				elif h(child) == h(next_node):
					best.append(child)
			

		if next_node == node:
			finished = True
		else:
			node = random.choice(best)
			tam += 1

	if display:
		print("Goal was not found, ", len(explored), " paths have been expanded")
	return node, expanded_nodes, food_nodes, tam

def greedy_best_first_search(problem, h=None):
	"""Greedy Best-first graph search is an informative searching algorithm with f(n) = h(n).
	You need to specify the h function when you call best_first_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	node, expanded_nodes, food_nodes, tam = best_first_graph_search(problem, lambda n: h(n))
	return(node, expanded_nodes, food_nodes, tam)

def a_star_best_first_search(problem, h=None):
	"""A* search is an informative searching algorithm with f(n) = h(n) + g(n).
	You need to specify the h function when you call best_first_search, or else in your Problem subclass"""
	h = memoize(h or problem.h, 'h')
	node, expanded_nodes, food_nodes, tam = best_first_graph_search(problem, lambda n: h(n) + n.path_cost)
	return (node, expanded_nodes, food_nodes, tam)

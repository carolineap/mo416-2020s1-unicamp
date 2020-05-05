import search
from enum import Enum
from collections import deque
import math

from utils import *

#directions are different from the usual just for the plots make sense
class Actions(Enum):
	UP = (1, 0)
	DOWN = (-1, 0)
	RIGHT = (0, 1)
	LEFT = (0, -1)


class Problem(search.Problem):

	def __init__(self, maze, initial_state, goal_state, food_tile_cost=1, empty_tile_cost=1):
		self.maze = maze
		super().__init__(initial_state, goal_state)
		self.food_tile_cost = food_tile_cost
		self.empty_tile_cost = empty_tile_cost

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

# carol: para modelar com custos diferentes de caminho, basta criar outra classe 
# Problem que extende de search.Problem e dar override no método path_cost

class Node:
	"""A node in a search tree. Contains a pointer to the parent (the node
	that this is a successor of) and to the actual state for this node. Note
	that if a state is arrived at by two paths, then there are two nodes with
	the same state. Also includes the action that got us to this state, and
	the total path_cost (also known as g) to reach the node. Other functions
	may add an f and h value; see best_first_graph_search and astar_search for
	an explanation of how the f and h values are handled. You will not need to
	subclass this class."""

	def __init__(self, state, parent=None, action=None, path_cost=0):
		"""Create a search tree Node, derived from a parent by an action."""
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		self.depth = 0
		if parent:
			self.depth = parent.depth + 1

	def __repr__(self):
		return "<Node {}>".format(self.state)

	def __lt__(self, node):
		return self.state < node.state

	def expand(self, problem):
		"""List the nodes reachable in one step from this node."""
		return [self.child_node(problem, action)
				for action in problem.actions(self.state)]

	def child_node(self, problem, action):
		"""[Figure 3.10]"""
		next_state = problem.result(self.state, action)
		next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
		problem.path_cost(self.path_cost, self.state, action, next_state)
		return next_node

	def solution(self):
		"""Return the sequence of actions to go from the root to this node."""
		return [node.action for node in self.path()[1:]]

	def path(self):
		"""Return a list of nodes forming the path from the root to this node."""
		node, path_back = self, []
		while node:
			path_back.append(node)
			node = node.parent
		return list(reversed(path_back))

	# We want for a queue of nodes in breadth_first_graph_search or
	# astar_search to have no duplicated states, so we treat nodes
	# with the same state as equal. [Problem: this may not be what you
	# want in other contexts.]

	def __eq__(self, other):
		return isinstance(other, Node) and self.state == other.state

	def __hash__(self):
		# We use the hash value of the state
		# stored in the node instead of the node
		# object itself to quickly search a node
		# with the same state in a Hash Table
		return hash(self.state)


def depth_first_graph_search(problem):
	expanded_nodes = 0
	food_nodes = 0
	frontier = [(Node(problem.initial))]

	explored = set()
	while frontier:
		node = frontier.pop()
		expanded_nodes += 1
		food_nodes += problem.check_food(node.state)
		if problem.goal_test(node.state):
			return node, expanded_nodes, food_nodes
		explored.add(node.state)
		frontier.extend(child for child in node.expand(problem)
						if child.state not in explored and child not in frontier)
	return None, expanded_nodes, food_nodes


def breadth_first_graph_search(problem):
	expanded_nodes = 0
	food_nodes = 0
	node = Node(problem.initial)
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
				if problem.goal_test(child.state):
					return child, expanded_nodes, food_nodes
				frontier.append(child)
	return None, expanded_nodes, food_nodes

def best_first_graph_search(problem, f, display=False):
	expanded_nodes = 0
	food_nodes = 0
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			if display:
				print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
			return node, expanded_nodes, food_nodes
		expanded_nodes += 1
		food_nodes += problem.check_food(node.state)  
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None, expanded_nodes, food_nodes

def greedy_best_first_search(problem, h=None):
	"""Greedy Best-first graph search is an informative searching algorithm with f(n) = h(n).
	You need to specify the h function when you call best_first_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	node, expanded_nodes, food_nodes = best_first_graph_search(problem, lambda n: h(n))
	return(node, expanded_nodes, food_nodes)

def a_star_best_first_search(problem, h=None):
	"""A* search is an informative searching algorithm with f(n) = h(n) + g(n).
	You need to specify the h function when you call best_first_search, or else in your Problem subclass"""
	h = memoize(h or problem.h, 'h')
	node, expanded_nodes, food_nodes = best_first_graph_search(problem, lambda n: h(n) + n.path_cost)
	return (node, expanded_nodes, food_nodes)

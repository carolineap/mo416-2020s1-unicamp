from enum import Enum


class Actions(Enum):
	UP = (1, 0)
	DOWN = (-1, 0)
	RIGHT = (0, 1)
	LEFT = (0, -1)

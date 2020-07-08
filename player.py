from typing import Union
from snake import Snake
from PyUI import Color
from globe import *


class Player:
	def __init__(self):
		self.snake = None  # type: Union[None, Snake]
	
	def create_snake(self):
		self.snake = Snake((50, 50), Color(0, 0, 0), START_SPEED, 0, START_WIDTH)
		return self.snake

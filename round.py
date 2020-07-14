from PyUI import Color
from snake import Snake
import math
import random
import pygame
import time
from globe import *


class Round:
	def __init__(self, snakes):
		self.snakes = []
		self.player_id = {}
		self.amount = len(self.snakes)
		self.score = {}
		self.start = False
		for snake in snakes:
			self.add_snake(snake)

	def add_snake(self, snake):
		self.snakes.append(snake)
		self.player_id[snake] = self.amount
		self.score[snake] = 0
		self.amount += 1

	def initialize(self):
		center = (WIDTH / 2, HEIGHT / 2)
		alpha = 0
		degree = 360 / self.amount
		color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		while color.is_similar(Color(BACKGROUND_COLOR)):
			color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		for i in range(self.amount):
			x = center[0] + math.cos(alpha * (math.pi / 180)) * (WIDTH / 2.5)
			y = center[1] + math.sin(alpha * (math.pi / 180)) * (HEIGHT / 2.5)
			c = color
			self.snakes[i].initialize(x, y, c)
			alpha += degree
			for k in range(len(color)):
				color[k] += int(255 / self.amount)
				color[k] %= 255

	def add_score(self, player, addition):
		self.score[player] += addition

	def start_game(self):
		self.start = True
		self.initialize()

		for snake in self.snakes:
			print("snake:")
			print("x: ", snake.head.x)
			print("y: ", snake.head.y)
			print("color: ", snake.color)


def test():
	window = pygame.display.set_mode((500, 500))
	snakes = [(Snake((0, 0), Color(255, 255, 255), START_SPEED, 0, START_WIDTH)) for i in range(10)]
	round = Round(snakes)
	print("amount: ", round.amount)
	round.initialize()

	window.fill(BACKGROUND_COLOR)
	for player in round.snakes:
		player.draw(pygame.display.get_surface())
	pygame.display.update()
	for player in round.snakes:
		print('x: ', player.head.x, ' y: ', player.head.y, ' color: ', player.color)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			print("quit")
			pygame.quit()
	time.sleep(10)


if __name__ == "__main__":
	test()

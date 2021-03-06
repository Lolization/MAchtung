from PyUI import Color
from snake import Snake
import random
import pygame
import time
from globe import *


class Round:
	def __init__(self, snakes):
		self.snakes = []
		self.player_id = {}
		self.amount = 0
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
		colors = [Color(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])]
		color = Color.random_color()
		color = self.get_random_color(colors, color)
		for i in range(self.amount):
			x = center[0] + math.cos(degree_to_rad(alpha)) * (WIDTH / 2.5)
			y = center[1] - math.sin(degree_to_rad(alpha)) * (HEIGHT / 2.5)
			c = color.copy()
			self.snakes[i].initialize(x, y, c, alpha + 180)
			alpha += degree
			color = Color.random_color()
			color = self.get_random_color(colors, color)

	@staticmethod
	def get_random_color(colors, color):
		colors.append(color)
		i = 0
		while i < len(colors):
			while color.is_similar(colors[i]):
				color = Color.random_color()
				i = 0
			i += 1
		colors[-1] = color
		return color

	def add_score(self, player, addition):
		self.score[player] += addition

	def start_game(self):
		self.start = True
		self.initialize()

		print("The snakes are: ")
		for snake in self.snakes:
			print("     ", snake)
			print("     x: ", snake.head.x)
			print("     y: ", snake.head.y)
			print("     alpha: ", snake.alpha)


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

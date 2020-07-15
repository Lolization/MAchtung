from typing import List, Union

import pygame

from account import Account
from network import *
from PyUI import *
import pickle
from globe import *
from player import Player
from room import Room
import time

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
players = []
me = None
n = None  # type: Union[None, Network]
i = 0  # Shitty solution for load


# Graphics
def redraw_window(window):
	window.fill(BACKGROUND_COLOR)
	for player in players:
		player.draw(window)
	me.draw(window)
	pygame.display.update()


def on_hover(view):
	view.text.set_color(Color(0, 0, 0))


def on_unhover(view):
	view.text.set_color(Color(255, 255, 255))


def load(screen):
	global i
	i += 1
	i %= 5
	for k in range(i):
		pygame.draw.circle(screen, (255, 255, 255), (int((WIDTH / 2) - 15 + (k * 5)), 120), 2)


def is_everyone_ready(accounts):
	for acc in accounts:
		if not acc.ready:
			return False
	return True


def in_login(screen, clock):
	login = True

	def login_listener(view):
		nonlocal login
		print("Supposed to send username & password thingy")
		login = False

	title = TextView(130, 40, 250, 75) \
		.set_text("Achtung")

	username = EditText(150, 150, 200, 50) \
		.set_text("Username") \
		.set_draw_frame(True)

	password = EditText(150, 250, 200, 50) \
		.set_text("Password") \
		.set_draw_frame(True)

	login_btn = Button(350, 400, 100, 50) \
		.set_text("Login!") \
		.set_on_click_listener(login_listener) \
		.set_on_hover_listener(on_hover) \
		.set_on_unhover_listener(on_unhover)

	while login:
		screen.fill(BACKGROUND_COLOR)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				login = False
				pygame.quit()
				break
		
		ViewHandler.handle_view_events(events)
		
		ViewHandler.render_views(screen)
		pygame.display.update()
		clock.tick(60)

	return username.text.text, password.text.text


def in_lobby(screen, clock, rooms):
	# type: (pygame.display, pygame.time.Clock, List[Room]) -> Union[None, Room]
	lobby = True
	data = None
	ViewHandler.clear_views()

	def new_room_listener(view):
		nonlocal lobby
		nonlocal data
		
		n.send(("Create", 0))
		
		load(screen)
		
		created_room = n.receive()
		while created_room is None:
			created_room = n.receive()
		
		data = (created_room, [])
		lobby = False

	def room_listener(view):
		nonlocal lobby
		nonlocal data

		print("Supposed to send room thingy")
		room_num = btns.index(view)
		room_id = rooms[room_num].id
		n.send(("Join", room_id))
		
		load(screen)

		accs = n.receive()
		while accs is None:
			accs = n.receive()

		data = (rooms[room_num], accs)
		lobby = False

	title = TextView(150, 50, 200, 50) \
		.set_text("Achtung")

	btns = []

	for i, room in enumerate(rooms):
		btns.append(Button(WIDTH / 2 - 150, 250 + (i * 75), 300)
		            .set_text(f"Room #{room.id + 1}")
		            .set_on_click_listener(room_listener)
		            .set_on_hover_listener(on_hover)
		            .set_on_unhover_listener(on_unhover))

	create_room_btn = Button(300, 400, 175, 50) \
		.set_text("Create A Room") \
		.set_on_click_listener(new_room_listener) \
		.set_on_hover_listener(on_hover) \
		.set_on_unhover_listener(on_unhover)

	while lobby:
		new_room = n.receive()
		if new_room:
			print("got room")
			rooms.append(new_room)
			btns.append(Button(WIDTH / 2 - 150, 250 + ((len(rooms) - 1) * 75), 300)
			            .set_text(f"Room #{new_room.id + 1}")
			            .set_on_click_listener(room_listener)
			            .set_on_hover_listener(on_hover)
			            .set_on_unhover_listener(on_unhover))

		screen.fill(BACKGROUND_COLOR)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				lobby = False
				pygame.quit()
				break

		ViewHandler.handle_view_events(events)

		ViewHandler.render_views(screen)
		pygame.display.flip()
		clock.tick(60)

	return data


def in_room(screen: pygame.display, clock: pygame.time.Clock, my_acc: Account, accounts: List[Account], room: Room) -> None:
	ViewHandler.clear_views()
	is_in_room = True
	sent_ready = False

	def game_listener(view):
		nonlocal is_in_room
		nonlocal sent_ready

		if not sent_ready:
			n.send("ready")
			print("Sent ready")
			sent_ready = True

	play = Button(WIDTH / 2 - 150, 50, 300) \
		.set_text("Ready") \
		.set_on_click_listener(game_listener) \
		.set_on_hover_listener(on_hover) \
		.set_on_unhover_listener(on_unhover)

	my_textview = TextView(50, 150, 200).set_text(my_acc.username)

	accounts_display = []  # type: List[TextView]

	for i, acc in enumerate(accounts):  # type: int, Account
		accounts_display.append(TextView(WIDTH / 2, 200 + (i * 50), 300)
		                        .set_text(acc.username))

	while is_in_room:
		data = n.receive()
		if data:
			if type(data) == Account:
				new_account = data
				print("got another acc")
				accounts.append(new_account)
				accounts_display.append(TextView(WIDTH / 2, 200 + ((len(accounts) - 1) * 50), 300)
				                        .set_text(new_account.username))
			elif data == "ready":
				print("Got ready")
				room.running = True
				is_in_room = False
			else:
				print("-----------Weird data!!!!:", data)

		screen.fill(BACKGROUND_COLOR)
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				is_in_room = False
				pygame.quit()
				break

		ViewHandler.handle_view_events(events)

		ViewHandler.render_views(screen)
		pygame.display.update()
		clock.tick(60)


def main():
	global me, players, n

	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	pygame.display.set_caption("MAAAAAAAAAAAAchtung")

	# Draw Log-in and Register while not connected
	username, password = in_login(screen, clock)

	n = Network()
	n.send((username, password))

	data = n.receive()
	while data is None:
		data = n.receive()

	my_acc, rooms = data

	# Draw Main Menu while not in a room
	room, accs = in_lobby(screen, clock, rooms)

	# Draw the room
	in_room(screen, clock, my_acc, accs, room)

	while not room.running:  # Wait for everyone to say "ready"
		print("waiting")
		pass

	message = n.receive()
	while message is None:
		message = n.receive()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				print("quit")
				pygame.quit()
	print(message)
	me, players = message
	print("me: ", me)
	print("players: ", players)

	run = True
	redraw_window(win)
	while run:
		clock.tick(60)
		n.send(me.head)
		heads = n.receive()
		while heads is None:
			heads = n.receive()

		# print('heads: ', heads)
		for i in range(len(players)):
			player = players[i]
			head = heads[i]
			player.add(head)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				print("quit")
				pygame.quit()

		for player in players + [me]:
			for head in heads + [me.head]:
				if player.lost(head, win):
					print("lost")
					n.send("lost")
					run = False

		me.move()
		# redraw_window(win)
		'''
		for head in heads + [me.head]:
			if not head.gap:
				head.draw(win)
			else:
				redraw_window(win)
		'''

		for player in players + [me]:
			head = player.head
			if len(player.body) > 1:
				point = player.body[-2]
				if point.gap:
					pygame.draw.circle(win, BACKGROUND_COLOR, (int(point.x), int(point.y)), int(point.radius))
			if len(player.body) > 10:
				p = player.body[-10]
				if player.is_after_gap(p) or player.is_before_gap(p):
					p.draw(win)
			head.draw(win)

		pygame.display.update()


if __name__ == "__main__":
	main()

import pygame
from network import *
from PyUI import *
import pickle
from globe import *

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
players = []
me = None
n = None


def redraw_window(window):
	window.fill((255, 255, 255))
	for player in players:
		player.draw(window)
	me.draw(window)
	pygame.display.update()


def in_login(screen, clock):
	login = True
	
	def login_listener(view):
		nonlocal login
		print("Supposed to send username & password thingy")
		login = False
	
	username = EditText(150, 150, 200, 50) \
		.set_text("Username")
	
	password = EditText(150, 250, 200, 50) \
		.set_text("Password")
	
	login_btn = Button(200, 350, 100, 50) \
		.set_text("Login!") \
		.set_on_click_listener(login_listener) \
		.set_rainbow(True)
	
	while login:
		screen.fill([0, 0, 0])
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
	lobby = True
	ViewHandler.clear_views()
	
	def new_room_listener(view):
		nonlocal lobby
		n.send(("Create", 0))
		lobby = False
	
	def room_listener(view):
		nonlocal lobby
		print("Supposed to send room thingy")
		room_num = btns.index(view)
		room_id = rooms[room_num].id
		n.send(("Join", room_id))
		lobby = False
	
	title = TextView(WIDTH / 2 - 50, 50, 100) \
		.set_text("MAAchtung")
	
	btns = []
	
	print(len(rooms))
	for i, room in enumerate(rooms):
		btns.append(Button(WIDTH / 2 - 50, 250 + (i * 75), 100)
					.set_text(f"Room #{room.id}")
					.set_on_click_listener(room_listener))
	
	create_room_btn = Button(WIDTH / 4, 250) \
		.set_text("Create A Room Buddy!") \
		.set_on_click_listener(new_room_listener)
	
	i = 0
	while lobby:
		new_room = n.receive()
		if new_room:
			print("got room")
			rooms.append(new_room)
			btns.append(Button(WIDTH / 2 - 50, 250 + ((len(rooms) - 1) * 75), 100)
						.set_text(f"Room #{new_room.id}")
						.set_on_click_listener(room_listener))
		
		screen.fill([0, 0, 0])
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				lobby = False
				pygame.quit()
				break
		
		for k in range(i):
			pygame.draw.circle(screen, (255, 255, 255), (int((WIDTH / 2) - 20 + (k * 5)), 120), 2)
		ViewHandler.handle_view_events(events)
		
		ViewHandler.render_views(screen)
		pygame.display.flip()
		clock.tick(7)
		i += 1
		i %= 5


def in_room(screen, clock):
	ViewHandler.clear_views()
	room = True
	
	def game_listener(view):
		nonlocal room
		room = False
	
	play = Button(WIDTH / 2 - 25, 50) \
		.set_text("Ya wanna play boi?") \
		.set_on_click_listener(game_listener)
	
	while room:
		screen.fill([0, 0, 0])
		events = pygame.event.get()
		
		for event in events:
			if event.type == pygame.QUIT:
				lobby = False
				pygame.quit()
				break
		
		ViewHandler.handle_view_events(events)
		
		ViewHandler.render_views(screen)
		pygame.display.update()
		clock.tick(60)


def main():
	global me, players, n
	
	pygame.init()
	ViewHandler.set_pygame(pygame)
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	pygame.display.set_caption("MAAAAAAAAAAAAchtung")
	
	# Draw Log-in and Register while not connected
	username, password = in_login(screen, clock)
	
	n = Network()
	n.send((username, password))
	
	rooms = n.receive()
	while rooms is None:
		rooms = n.receive()
	
	# Draw Main Menu while not in a room
	in_lobby(screen, clock, rooms)
	
	# Draw the room
	in_room(screen, clock)
	
	me, players = n.receive()
	n.send("ready")
	
	run = True
	message = n.receive()
	while message is None:
		print(message)
		message = n.receive()
		pass
	me, players = message
	print("me: ", me)
	print("players: ", players)
	
	redraw_window(win)
	while run:
		clock.tick(60)
		heads = n.send(me.head)
		print("heads: ", heads)
		
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
		for head in heads + [me.head]:
			if not head.gap:
				head.draw(win)
			else:
				redraw_window(win)
		pygame.display.update()


if __name__ == "__main__":
	main()

import time
from socket import socket, AF_INET, SOCK_STREAM, error
from _thread import *
from typing import Union
import pickle
from room import Room
from game import Game
from globe import *
from account import Account

# TODO - proper game cycle:
# TODO - 1. points counter
# TODO - 2. menu
# TODO - 3. messages to the user (you win, you lose, etc.)

# TODO - create an .exe file

rooms = []
s = None
lobby_conns = []
room_cons = {}


def main():
	# TODO - organize, annoy Termiland
	
	create_socket()
	while True:
		conn, address = s.accept()
		lobby_conns.append(conn)  # TODO: Email and pass thing verification
		print("Connected to:", address)
		
		username, password = pickle.loads(conn.recv(1048))
		print(username, password, " entered")
		# TODO: Check if account already exists (Wrong pass, get info, etc.)
		account = Account(username, password)
		start_new_thread(threaded_client, (conn, account))


def create_socket():
	global s
	s = socket(AF_INET, SOCK_STREAM)
	
	try:
		s.bind(("0.0.0.0", PORT))
	except error as e:
		str(e)
	
	s.listen(2)
	print("Waiting for a connection, Server Started")


def get_room(identifier):
	for room in rooms:
		if room.id == identifier:
			return room
	
	return None


def create_room(connection, acc):
	new_room = Room()\
		.add_account(acc)
	lobby_conns.remove(connection)
	for con in lobby_conns:
		con.sendall(pickle.dumps(new_room))
	connection.sendall(pickle.dumps(new_room))
	rooms.append(new_room)
	room_cons[new_room.id] = [connection]
	return new_room


def join_room(connection: socket, acc: Account, room_id: int) -> Room:
	
	room = get_room(room_id)  # type: Room
	for con in room_cons[room_id]:  # type: socket
		con.sendall(pickle.dumps(acc))
	connection.sendall(pickle.dumps(room.accounts))
	room.add_account(acc)
	room_cons[room_id].append(connection)
	return room


def threaded_client(conn: socket, account: Account) -> None:
	global s
	
	while True:
		conn.sendall(pickle.dumps((account, rooms)))
		room = None  # type: Union[None, Room]
		
		lobby = True
		while lobby:
			msg = pickle.loads(conn.recv(1042))
			if msg:
				action, placeholder = msg
				if action == "Join":
					room_id = placeholder
					room = join_room(conn, account, room_id)
					lobby = False
				elif action == "Create":
					room = create_room(conn, account)
					lobby = False
				
				else:
					print("PLEASE HELP ME")
		
		msg = pickle.loads(conn.recv(1024))
		while msg is None:
			msg = pickle.loads(conn.recv(1024))
		
		if msg == "ready":
			account.ready = True
			if room.is_ready():
				for con in room_cons[room.id]:
					con.sendall(pickle.dumps("ready"))
				room.running = True
		
		while not room.running:
			pass
		
		print("round started")
		players = [account.player for account in room.accounts]
		player_num = room.accounts.index(account)
		if room.game is None:
			game = Game(players)
			room.game = game
		if room.game.current_round is None:
			current_round = room.game.create_round()
		else:
			current_round = room.game.current_round
		
		initial_players = []
		for i in range(len(current_round.snakes)):
			if i != player_num:
				initial_players.append(current_round.snakes[i])
		
		if not current_round.start:
			current_round.start_game()
			print("started game")
		message = (current_round.snakes[player_num], initial_players)
		print(message)
	
		time.sleep(1)
		conn.sendall(pickle.dumps(message))
		
		while True:
			try:
				reply = []
				data = pickle.loads(conn.recv(1042))
				if data == "lost":
					break
				current_round.snakes[player_num].add(data)
				
				if not data:
					print("Disconnected")
					break
				else:
					for i in range(len(current_round.snakes)):
						if i != player_num:
							reply.append(current_round.snakes[i].head)
				
				conn.sendall(pickle.dumps(reply))
			except error as e:
				print(e)
				break
		
		lobby_conns.append(conn)


if __name__ == "__main__":
	main()

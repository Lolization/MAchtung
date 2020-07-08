from socket import socket, AF_INET, SOCK_STREAM, error
from _thread import *
from typing import Union
from snake import Snake
import sys
import pickle
from room import Room
from round import Round
from game import Game
from player import Player
from globe import *
from account import Account

# TODO - proper game cycle:
# TODO - 1. points counter
# TODO - 2. menu
# TODO - 3. messages to the user (you win, you lose, etc.)

# TODO - massive amount of data needs to be received (entire list of points)
# TODO - create an .exe file

P1_COLOR = P2_COLOR = (20, 20, 20)
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
		
		username, password = pickle.loads(conn.recv(2048))
		print(username, password)
		# TODO: Check if account already exists (Wrong pass, get info, etc.)
		account = Account(conn, username, password)
		print(account)
		print(rooms)
		conn.sendall(pickle.dumps((account, rooms)))
		start_new_thread(threaded_client, (conn, account))


def create_socket():
	global s
	s = socket(AF_INET, SOCK_STREAM)
	
	try:
		s.bind((SERVER, PORT))
	except error as e:
		str(e)
	
	s.listen(2)
	print("Waiting for a connection, Server Started")


def get_room(iden):
	for room in rooms:
		if room.id == iden:
			return room
	
	return None


def create_room(con, acc, room):
	new_room = room.add_account(acc)
	lobby_conns.remove(con)
	for con in lobby_conns:
		con.sendall(pickle.dumps(new_room))
	con.sendall(pickle.dumps([]))
	rooms.append(new_room)
	room_cons[new_room.id] = [con]
	return new_room


def join_room(connection, acc, room_id):
	# type: (socket, Account, int) -> Room
	
	room = get_room(room_id)  # type: Room
	for con in room_cons[room_id]:  # type: socket
		con.sendall(pickle.dumps(acc))
	connection.sendall(pickle.dumps(room.accounts))
	room.add_account(acc)
	return room


def threaded_client(conn, account):
	global s
	room = None  # type: Union[None, Room]
	
	lobby = True
	while lobby:
		msg = pickle.loads(conn.recv(4096))
		if msg:
			print(msg)
			action, room_id = msg
			if action == "Join":
				room = join_room(conn, account, room_id)
				lobby = False
			elif action == "Create":
				print("create room gever")
				room = create_room(conn, account, room_id)
				lobby = False
			
			else:
				print("PLEASE HELP ME")
	
	pickle.dumps(room.accounts)
	
	while not room.running:
		pass
	
	print("round started")
	player_num = account.room.accounts.index(account)
	current_round = room.game.create_round()
	
	initial_players = []
	for i in range(len(current_round.snakes)):
		if i != player_num:
			initial_players.append(current_round.snakes[i])
	message = (current_round.snakes[player_num], initial_players)
	print(message)
	conn.send(pickle.dumps(message))
	
	while True:
		try:
			reply = []
			data = pickle.loads(conn.recv(4096))
			print('head: ', data)
			if data == "lost":
				break
			current_round.snakes[player_num].add(data)
			
			if not data:
				print("Disconnected")
				break
			else:
				print(len(current_round.snakes))
				for i in range(len(current_round.snakes)):
					if i != player_num:
						print("entered")
						reply.append(current_round.snakes[i].head)
				print("Received: ", data)
				print("Sending : ", reply)
			
			conn.sendall(pickle.dumps(reply))
		except error as e:
			print(e)
			break
	
	print("Lost connection")
	conn.close()


if __name__ == "__main__":
	main()

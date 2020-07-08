import socket
from _thread import *
from snake import Snake
import sys
import pygame
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
round = None
s = None


def main():
    global round
    # create_players()
    # TODO - organize, annoy Termiland

    create_socket()
    player_amount = 0
    while True:
        conn, address = s.accept()
        print("Connected to:", address)

        username, password = pickle.loads(conn.recv(2048))
        account = Account(username, password)
        start_new_thread(threaded_client, (conn, account, player_amount))


def create_socket():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((SERVER, PORT))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")


def create_players():
    snake1 = Snake((100, 100), P1_COLOR, START_SPEED, 0, START_WIDTH)
    snake2 = Snake((250, 250), P2_COLOR, START_SPEED, 0, START_WIDTH)
    snakes = [snake1, snake2]


def threaded_client(conn, account, player_num):
    global round, s
    '''
    in_room = False
    while not in_room:
        room_message = conn.recv(4096)
        print(room_message.decode())
        in_room = True
    '''

    while not round.start:
        pass

    print("round started")
    # print("snakes: ", round.snakes)

    initial_players = []
    for i in range(len(round.snakes)):
        if i != player_num:
            initial_players.append(round.snakes[i])
    message = (round.snakes[player_num], initial_players)
    print(message)
    conn.send(pickle.dumps(message))

    while True:
        try:
            reply = []
            data = pickle.loads(conn.recv(4096))
            print('head: ', data)
            if data == "lost":
                pygame.quit()
                break
            round.snakes[player_num].add(data)

            if not data:
                print("Disconnected")
                break
            else:
                print(len(round.snakes))
                for i in range(len(round.snakes)):
                    if i != player_num:
                        print("entered")
                        reply.append(round.snakes[i].head)
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except error as e:
            break

    print("Lost connection")
    conn.close()


if __name__ == "__main__":
    main()

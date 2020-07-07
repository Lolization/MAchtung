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

# TODO - proper game cycle:
# TODO - 1. points counter
# TODO - 2. menu
# TODO - 3. messages to the user (you win, you lose, etc.)

# TODO - massive amount of data needs to be received (entire list of points)
# TODO - create an .exe file

SERVER = "10.0.0.28"
PORT = 5555

P1_COLOR = (179, 222, 238)
P2_COLOR = (184, 102, 81)
snakes = []
players = [Player(), Player()]
s = None


def main():
    global players
    create_players()
    # TODO - organize
    room = Room()
    for i in range(len(players)):
        players[i].snake = snakes[i]
    game = Game(players)
    room.game = game
    round = Round(snakes)

    create_socket()
    current_player = 0
    while True:
        conn, address = s.accept()
        print("Connected to:", address)

        start_new_thread(threaded_client, (conn, current_player))
        current_player += 1


def create_socket():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("entered")
        s.bind((SERVER, PORT))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")


def create_players():
    global snakes
    snake1 = Snake((100, 100), P1_COLOR, 0.9, 0, 8)
    snake2 = Snake((250, 250), P2_COLOR, 0.9, 0, 8)
    snakes = [snake1, snake2]


def threaded_client(conn, player_num):
    global s
    initial_players = []
    for i in range(len(snakes)):
        if i != player_num:
            initial_players.append(snakes[i])
    message = (snakes[player_num], initial_players)
    print(message)
    conn.send(pickle.dumps(message))

    while True:
        try:
            reply = []
            head = pickle.loads(conn.recv(2048))
            print('head: ', head)
            if head == "lost":
                pygame.quit()
                break
            snakes[player_num].add(head)

            if not head:
                print("Disconnected")
                break
            else:
                print(len(snakes))
                for i in range(len(snakes)):
                    if i != player_num:
                        print("entered")
                        reply.append(snakes[i].head)
                print("Received: ", head)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except error as e:
            break

    print("Lost connection")
    conn.close()


if __name__ == "__main__":
    main()

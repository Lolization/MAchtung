import pygame
from network import *
from PyUI import *
import pickle
from globe import *

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
players = []
me = None


def redraw_window(window):
    window.fill((255, 255, 255))
    for player in players:
        player.draw(window)
    me.draw(window)
    pygame.display.update()


def in_login(screen, clock):
    login = True

    def login_listener():
        nonlocal login
        print("Supposed to send username & password thingy")
        login = False

    username = EditText(150, 150, 200, 50) \
        .set_text("Username") \

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


def in_lobby(screen, clock):
    lobby = True
    ViewHandler.clear_views()

    def room_listener():
        nonlocal lobby
        print("Supposed to send room thingy")
        lobby = False

    title = TextView(WIDTH / 2 - 50, 50, 100) \
        .set_text("MAAchtung")

    room1 = Button(WIDTH / 2 - 50, 250, 100) \
        .set_text("Room #1") \
        .set_on_click_listener(room_listener)

    i = 0
    while lobby:
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

    def game_listener():
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
    global me, players

    pygame.init()
    ViewHandler.set_pygame(pygame)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Draw Log-in and Register while not connected
    username, password = in_login(screen, clock)
    print(username)
    print(password)

    # Draw Main Menu while not in a room
    in_lobby(screen, clock)

    # Draw the room
    in_room(screen, clock)

    n = Network()
    me, players = receive(n.client)
    n.send(pickle.dumps((username, password)))
    n.send("ready")

    run = True
    message = receive(n.client)
    while message is None:
        print(message)
        message = receive(n.client)
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

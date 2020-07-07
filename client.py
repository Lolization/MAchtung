import pygame
from network import Network
import network

# TODO - lose when bumping into the enemy

WIDTH = 500
HEIGHT = 500
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


def main():
    global me, players
    run = True
    n = Network()
    message = n.get_players()
    while message is None:
        print(message)
        message = network.receive(n.client)
        pass
    me, players = n.get_players()
    print("me: ", me)
    print("players: ", players)
    clock = pygame.time.Clock()

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


main()

class Game:
    def __init__(self, players):
        self.players = players
        self.points = []
        for i in range(len(players)):
            self.points[i] = 0

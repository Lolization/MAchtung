from round import Round


class Game:
    def __init__(self, players):
        self.players = players
        self.points = []
        for i in range(len(players)):
            self.points[i] = 0

    def create_round(self):
        new_round = Round()

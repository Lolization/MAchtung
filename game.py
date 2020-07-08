from round import Round


class Game:
	def __init__(self, players):
		self.players = players
		self.current_round = None
	
	def create_round(self):
		
		snakes = []
		for player in self.players:
			snakes.append(player.create_snake())
		new_round = Round(snakes)
		self.current_round = new_round
		return new_round

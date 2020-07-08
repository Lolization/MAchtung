from player import Player


class Account:
	def __init__(self, connection, username, password):
		self.con = None
		self.username = username
		self.password = password
		self.level = 1
		self.xp = 0
		self.powerups = []
		self.room = None
		self.ready = False
		self.player = Player()
	
	def add_powerup(self, powerup):
		self.powerups.append(powerup)
	
	def update_player(self):
		pass

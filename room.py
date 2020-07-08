from account import Account


class Room:
	id = 0
	
	def __init__(self):
		self.id = Room.id
		Room.id += 1
		self.accounts = []
		self.game = None
		self.running = False
	
	def add_account(self, account):
		self.accounts.append(account)
		return self

from typing import List, Union
import account
import game


class Room:
	id = 0
	
	def __init__(self):
		self.id = Room.id
		Room.id += 1
		print(Room.id)
		
		self.accounts: List[account.Account] = []
		self.game: Union[None, game.Game] = None
		self.running: bool = False
	
	def add_account(self, acc: account.Account):
		self.accounts.append(acc)
		return self
	
	def is_ready(self):
		for acc in self.accounts:
			if not acc.ready:
				return False
		return True

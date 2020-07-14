from __future__ import annotations
from typing import List, Union
from Powerup import Powerup
from player import Player


class Account:
	def __init__(self, username: str, password: str):
		self.username: str = username
		self.password: str = password
		self.level: int = 1
		self.xp: int = 0
		self.powerups: List[Powerup] = []
		self.room_id: int = -1
		self.ready: bool = False
		self.player: Player = Player()
	
	# Add a powerup to the account
	def add_powerup(self, powerup: Powerup) -> Account:
		self.powerups.append(powerup)
		return self
	
	def update_player(self):
		pass

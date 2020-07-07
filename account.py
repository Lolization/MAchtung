class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.level = 1
        self.xp = 0
        self.powerups = []

    def add_powerup(self, powerup):
        self.powerups.append(powerup)

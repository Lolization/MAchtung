from account import Account


class Room:
    def __init__(self):
        self.accounts = []
        self.game = None
        self.running = False

    def add_account(self, account):
        self.accounts.append(account)

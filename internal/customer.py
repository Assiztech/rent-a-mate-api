from internal.account import Account

class Customer(Account):
    def __init__(self, username: str, password: str, gender: str, location: str) -> None:
        super().__init__(username, password, gender, location)
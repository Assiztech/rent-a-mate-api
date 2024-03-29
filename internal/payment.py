from internal.account import UserAccount

class Payment:
    def __init__(self, amount: int) -> None:
        self.__amount = amount

    def pay(self, sender: UserAccount, receiver: UserAccount) -> None | bool:
        if sender.amount < self.__amount:
            return False
        sender - self.__amount
        receiver + self.__amount
        
    @property
    def amount(self) -> int:
        return self.__amount
import datetime

from internal.account import Account
from internal.availability import Availablility
from internal.review import Review

class Mate(Account):
    def __init__(self, username: str, password: str, gender: str, location: str, amount: int=0):
        super().__init__(username, password, gender, location)
        self.__availablility_list: list[Availablility] = []
        self.__review_list = []
        self.__booked_customer = None
        self.__amount = amount
    @property
    def availablility_list(self) -> list[Availablility]:
        return self.__availablility_list
    @property
    def booked_customer(self) -> Account:
        return self.__booked_customer
    @property
    def amount(self) -> int:
        return self.__amount
    
    def add_availablility(self, date: datetime, detail: str) -> Availablility:
        availablility: Availablility = Availablility(date, detail)
        self.__availablility_list.append(availablility)
        return availablility
    
    def search_availablility(self, year: int, month: int, day: int) -> Availablility | None:
        for availablility in self.__availablility_list:
            if availablility.check_available(year, month, day):
                return availablility
        return None
    
    def book(self, customer: Account, year: int, month: int, day: int) -> Account | None:
        if isinstance(self.__booked_customer, type(None)):
            for availablility in self.__availablility_list:
                if availablility.check_available(year, month, day):
                    self.__availablility_list.remove(availablility)
                    self.__booked_customer: Account = customer
                    return self.__booked_customer
        return None

    def confirm_booking(self):
        pass
    
    def update_availablility(self):
        pass
    
    def add_post(self):
        pass
    
    def withdraw(self):
        pass
    
    def set_availablility(self):
        pass
    
    def add_review_mate(self, customer_id, message, star) -> Review | None:
        if not isinstance(customer_id , str):
            return None
        review = Review(customer_id, message, star)
        self.__review_list.append(review)
        return review
from uuid import uuid4, UUID
from datetime import datetime
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, username, password, pic_url) -> None:
        self._id: UUID = uuid4()
        self._display_name : str = username
        self._username: str = username
        self._password: str = password
        self._timestamp = datetime.now()
        self._pic_url: str = pic_url

    @abstractmethod
    def get_account_details(self) -> dict:
        pass

    @property
    def username(self) -> str:
        return self._username
    @property
    def display_name(self) -> str:
        return self._display_name
    @property
    def id(self) -> UUID:
        return self._id
    @property
    def password(self) -> str:
        return self._password
    @property
    def age(self) -> str:
        return self._age
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    @property
    def pic_url(self) -> str:
        return self._pic_url
    @pic_url.setter
    def pic_url(self, url):
        self._pic_url = url
    @property
    def password(self) -> str:
        return self._password
    @age.setter
    def age(self, new_age):
        self._age = new_age

    def validate_account_id(self, id):
        return str(self.id) == id
    
    def add_pic_url(self, pic_url):
        self.pic_url = pic_url
    
class UserAccount(Account):
    def __init__(self, username: str, password: str, gender: str, location: str, pic_url: str = "", amount: int = 0, age: int = 18) -> None:
        super().__init__(username, password, pic_url)
        self._amount: int = amount
        self._gender: str = gender
        self._location: str = location
        self._age: int = age
        self._transaction_list: list = []
        self._booking_list: list = []

    @property
    def gender(self) -> str:
        return self._gender
    @property
    def booking_list(self) -> list:
        return self._booking_list  
    @property
    def display_name(self) -> str:
        return self._display_name
    @display_name.setter
    def display_name(self, name):
        self._display_name = name
    @property
    def id(self) -> UUID:
        return self._id
    @property
    def transaction_list(self) -> list:
        return self._transaction_list
    @property
    def amount(self) -> int:
        return self._amount
    @amount.setter
    def amount(self, amount):
        self._amount = amount
    @property
    def location(self) -> str:
        return self._location
    @location.setter
    def location(self, location):
        self._location = location
    
    def get_account_details(self) -> dict:
        from internal.customer import Customer
        return {
            "id": str(self._id),
            "displayname": self._display_name,
            "username": self._username,
            "pic_url": self._pic_url,
            "role": "customer" if isinstance(self, Customer) else "mate", 
            "gender": self._gender,
            "location": self._location,
            "timestamp": self._timestamp.strftime("%d/%m/%Y %H:%M:%S"),
            "age": self._age,
        }
    
    def add_transaction(self, transaction) -> None:
        from internal.transaction import Transaction
        if not isinstance(transaction, Transaction):
            raise TypeError(f"Expected transaction, but got {type(transaction)} instead.")
        self._transaction_list.append(transaction)
        return transaction
    
    def __add__(self, amount: int) -> int:
        self._amount += amount
        return self._amount

    def __sub__(self, amount: int) -> int:
        if self._amount - amount < 0:
            self._amount = 0
        else:
            self._amount -= amount
        return self._amount
    
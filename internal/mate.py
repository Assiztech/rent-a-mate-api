import datetime
from internal.account import UserAccount
from internal.availability import Availability
from internal.review import Review
from internal.customer import Customer

class Mate(UserAccount):
    def __init__(self, username: str, password: str, gender: str, location: str, price: int=0):
        super().__init__(username, password, gender, location)
        self.__availability_list: list[Availability] = []
        self.__review_list: list[Review] = []
        self.__price = price
        self.__rented_count = 0
        self.__max_availability = 6
        self.__review_customer_list: list[Customer] = []

    @property
    def availability_list(self) -> list[Availability]:
        return self.__availability_list
    @property   
    def review_customer_list(self) -> list[Customer]:
        return self.__review_customer_list
    @property
    def price(self) -> int:
        return self.__price
    @price.setter
    def price(self, price: int):
        self.__price = price
    @property
    def review_list(self) -> list[Review]:
        return self.__review_list
    
    def get_success_booking(self, booking_list: list) -> list:
        return [booking for booking in booking_list if booking.mate == self and booking.is_success]
    
    def add_availability(self, date: datetime, detail: str) -> Availability:
        availability: Availability = Availability(date, detail)
        self.__availability_list.append(availability)
        return availability
    
    def search_availability(self, year: int, month: int, day: int) -> Availability | None:
        if not self.is_availability_slot_valid():
            return None
        for availability in self.__availability_list:
            if availability.check_available(year, month, day):
                return availability
        return None
    
    def book(self, year: int, month: int, day: int) -> Availability | None:
        for availability in self.__availability_list:
            if availability.check_available(year, month, day):
                self.__availability_list.remove(availability)
                return availability
        return None

    def is_availability_slot_valid(self):
        return len(self.__availability_list) < self.__max_availability
    
    def get_average_review_star(self) -> float:
        sum: float = 0
        for review in self.__review_list:
            sum += review.star
        if len(self.__review_list):
            return round(sum / len(self.__review_list), 1)
        return -1.0

    def search_review_by_id(self, review_id: str) -> Review | None:
        for review in self.__review_list:
            if review.validate_id(review_id):
                return review
        return None

    def add_review_mate(self, reviewer: Customer, message: str, star: int) -> Review | None:
        if reviewer in self.__review_customer_list:
            return None
        review: Review = Review(reviewer, message, star)
        self.__review_list.append(review)
        return review
    
    def del_review_mate(self, review_id) -> Review | None:
        review: Review = self.search_review_by_id(review_id)
        if review == None:
            return None
        self.__review_list.remove(review)
        return review
    def add_rent_count(self):
        self.__rented_count =+ 1
    def get_review_amount(self) -> int:
        return len(self.__review_list)
    
    def get_review_mate(self) -> list[Review]:
        return self.__review_list
    
    def get_review_amount(self) -> int:
        return int(len(self.__review_list)) 
    
    def get_account_details(self) -> dict:
        return {
            "id": str(self.id),
            "username": self.username,
            "displayname":self.display_name,
            "pic_url": self.pic_url,
            "star": str(round(self.get_average_review_star(), 1)),
            "review_count":self.get_review_amount(),
            "role": "mate",
            "rent_count": self.__rented_count,
            "gender":self.gender,
            "location": self.location.capitalize(),
            "price": self.price,
            "amount" : self.amount,
            "timestamp": self._timestamp.strftime("%d/%m/%Y %H:%M:%S"),
            "age": self._age
        }
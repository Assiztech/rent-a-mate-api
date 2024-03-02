from internal.account import Account
from internal.message import Message
from internal.chat import Chat
from internal.booking import Booking
from internal.mate import Mate
from internal.customer import Customer
from internal.payment import Payment
from internal.transaction import Transaction
from internal.mate import Mate
# from internal.customer import Customer
from internal.review import Review
import datetime

class Controller:
    def __init__(self) -> None:
        self.__account_list: list = []
        self.__booking_list: list = []
        self.__chat_list = []

    def get_chat_list(self):
        return self.__chat_list
    
    def add_chat_room(self, chat):
        if not isinstance(chat, Chat):
            raise TypeError("chat must be Chat instances")
        self.__chat_list.append(chat)
    
    def search_account_by_id(self, id: str):
        for acc in self.__account_list:
            if(id == str(acc.id)):
                return acc
        return None

    def get_chat_by_owner_pair(self, owner1, owner2):
        if not (isinstance(owner1, Account) and isinstance(owner2, Account)):
            raise TypeError("owner1, owner2 must be Account instances")
        
        for chat in self.__chat_list:
            chat_owner1 = chat.get_owner1()
            chat_owner2 = chat.get_owner2()
            if((owner1 in [chat_owner1, chat_owner2]) and (owner2 in [chat_owner1, chat_owner2]) and (chat_owner1 != chat_owner2)):
                return chat
        
        return None

    def talk(self, sender_id: str, receiver_id: str, text: str):
        sender = self.search_account_by_id(sender_id)
        receiver = self.search_account_by_id(receiver_id)
        chat = self.get_chat_by_owner_pair(sender, receiver)
        if(chat != None):
            timestamp = datetime.datetime.now()
            msg = chat.save_chat_log(Message(sender, text, timestamp))
            return msg
        return None
    
    def delete_message(self, sender_id: str, receiver_id: str, message_id: str):
        sender = self.search_account_by_id(sender_id)
        receiver = self.search_account_by_id(receiver_id)
        chat = self.get_chat_by_owner_pair(sender, receiver)
        if(chat != None):
            msg_list = chat.delete_message(message_id)
            return msg_list
        return None
    
    def edit_message(self, sender_id: str, receiver_id: str, message_id: str, new_text: str):
        sender = self.search_account_by_id(sender_id)
        receiver = self.search_account_by_id(receiver_id)
        chat = self.get_chat_by_owner_pair(sender, receiver)
        if(chat != None):
            msg_list = chat.edit_message(message_id, new_text)
            return msg_list
        return None

    def retrieve_chat_log(self, sender_id, receiver_id):
        sender_acc = self.search_account_by_id(sender_id)
        receiver_acc = self.search_account_by_id(receiver_id)
        if not (isinstance(sender_acc, Account) and isinstance(receiver_acc, Account)):
            raise "No Acc found"
        chat = self.get_chat_by_owner_pair(sender_acc, receiver_acc)
        message_list = chat.get_message_list()
        all_chat_data = []
        for msg in message_list:
            sender_name = msg.get_sender_name()
            chat_data = {
                sender_name : {
                    "id" : msg.id,
                    "text" : msg.get_text(),
                    "timestamp" : msg.get_timestamp(),
                    "is_edit": msg.is_edit
                }
            }
            all_chat_data.append(chat_data)
        return all_chat_data   

    def get_receiver_chat_room_detail(self, sender_acc):
        detail = []
        if not (isinstance(sender_acc, Account)):
            raise TypeError("receiver_acc must be Account instances")
        for chat in self.__chat_list:
            chat_owner1 = chat.get_owner1()
            chat_owner2 = chat.get_owner2()
            if((sender_acc in [chat_owner1, chat_owner2]) and len(chat.get_message_list()) >= 1):
                latest_chat = chat.get_message_list()[-1]
                detail.append({
                        'account_detail' : latest_chat.get_sender_account().get_account_details(),
                        'latest_timestamp' : latest_chat.get_timestamp(),
                        'latest_text' : latest_chat.get_text(),
                })
        
        return detail
    

    def retrieve_chat_room(self, sender_id):
        sender_acc = self.search_account_by_id(sender_id)
        if not (isinstance(sender_acc, Account)):
            raise TypeError("No Acc found")
        detail = self.get_receiver_chat_room_detail(sender_acc)
        return detail
    @property
    def account_list(self) -> list:
        return self.__account_list
    @property
    def booking_list(self) -> list:
        return self.__booking_list

    async def add_instance(self):
        await self.add_customer("test1", "test1")
        await self.add_mate("test2", "test2")
        await self.add_customer("test3", "test3")
        await self.add_mate("test4", "test4")
        await self.add_customer("test5", "test5")
        await self.add_mate("test6", "test6")
        await self.add_customer("test7", "test7")
        await self.add_mate("test8", "test8")
        self.add_booking(self.account_list[0], self.account_list[1], 100)
        self.add_booking(self.account_list[2], self.account_list[3], 200)
        self.add_booking(self.account_list[4], self.account_list[5], 300)
        self.add_booking(self.account_list[6], self.account_list[7], 400)
        my_acc = await self.search_account_by_username("ganThepro")

        mate_acc = await self.add_mate("Mate1", "1234")
        mate_acc2 = await self.add_mate("Mate2", "1234")
        print("mate_acc: ", mate_acc.id)
        print("mate_acc: ", mate_acc2.id)

        self.add_chat_room(Chat(my_acc, mate_acc))
        self.add_chat_room(Chat(my_acc, mate_acc2))

    async def add_customer(self, username: str, password: str) -> Customer:
        existed_account: Account = await self.search_account_by_username(username)
        if existed_account != None:
            return None
        customer: Customer = Customer(username, password)
        self.__account_list.append(customer)
        return customer

    async def add_mate(self, username: str, password: str) -> Mate:
        existed_account: Account = await self.search_account_by_username(username)
        if existed_account != None:
            return None
        mate: Mate = Mate(username, password)
        self.__account_list.append(mate)
        return mate

    def add_booking(self, customer: Customer, mate: Mate, amount: int) -> Booking:
        booking: Booking = Booking(customer, mate, Payment(amount, False))
        self.__booking_list.append(booking)
        return booking

    async def search_account_by_username(self, username: str) -> Account | None:
        for account in self.__account_list:
            if account.username == username:
                return account
        return None
    
    async def search_booking_by_id(self, booking_id: str) -> Booking | None:
        for booking in self.__booking_list:
            if str(booking.id) == booking_id:
                return booking
        return None
    
    async def search_customer_by_id(self, customer_id: str) -> Account | None:
        for account in self.__account_list:
            if str(account.id) == customer_id:
                return account
        return None

    async def search_mate_by_id(self, mate_id: str) -> Mate | None:
        for account in self.__account_list:
            if str(account.id) == mate_id:
                return account
        return None
    
    async def search_booking(self, booking_id: str) -> dict:
        for booking in self.__booking_list:
            if str(booking.id) == booking_id:
                return booking.get_booking_detail()

    async def add_payment(self, booking_id: str) -> dict:
        booking: Booking = await self.search_booking_by_id(booking_id)
        if booking == None:
            return "Booking not found"
        customer: Customer = await self.search_customer_by_id(str(booking.customer.id))
        if customer == None:
            return "Customer not found"
        mate: Mate = await self.search_mate_by_id(str(booking.mate.id))
        if mate == None:
            return "Mate not found"
        payment: Payment = booking.payment
        payment.pay(customer, mate)
        self.add_chat_room(Chat(customer, mate))
        transaction: Transaction = Transaction(customer, mate, payment.amount)
        return transaction.get_transaction_details()
    
    def get_account_by_name(self, name: str) -> Account | None:
        for account in self.__account_list:
            if name in account.name:
                return account
        return None

    def get_mates(self) -> Account | None:
        mate_list = []
        for account in self.__account_list:
            if isinstance(account, Mate):
                mate_list.append(account)
        return mate_list

    # def get_customers(self) -> Account | None:
    #     customer_list = []
    #     for account in self.__account_list:
    #         if isinstance(account, Customer):
    #             customer_list.append(account)
    #     return None
    
    def add_review_mate(self, customer_id, mate_id, message, star) -> Review | None:
        for mate in self.get_mates():
            if (mate.id == mate_id):
                review = mate.add_review_mate(customer_id, message, star)
                return review
        return None
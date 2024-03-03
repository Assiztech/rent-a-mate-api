from internal.account import Account
from uuid import uuid4, UUID

class Message:
    def __init__(self, sender, text, timestamp) -> None:
        self.__id: UUID = uuid4()
        self.__sender = sender
        self.__text = text
        self.__timestamp = timestamp
        self.__is_edit = False
    
    @property
    def id(self) -> UUID:
        return self.__id
    
    @property
    def is_edit(self) -> bool:
        return self.__is_edit

    def get_sender_name(self) -> str:
        return self.__sender.username
    
    def get_sender_account(self) -> Account:
        return self.__sender
    
    def get_text(self) -> str:
        return self.__text
    
    def get_timestamp(self) -> str:
        return self.__timestamp.strftime("%d/%m/%Y %H:%M:%S")
    
    def set_text(self, text):
        self.__text = text
        self.__is_edit = True
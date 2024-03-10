from datetime import datetime
from internal.mate import Mate
from uuid import uuid4, UUID
class Post:
    def __init__(self, mate, description, picture) :
        self.__mate : Mate = mate
        self.__description = description
        self.__picture = picture
        self.__timestamp = datetime.datetime.now()
        self.__id : UUID= uuid4()

    @property
    def description(self):
        return self.__description
    @property
    def picture(self):
        return self.__picture
    @property
    def timestamp(self):
        return self.__timestamp
    @property
    def id(self):
        return self.__id
        
    def get_post_details(self) -> dict:
        return {
            "description": self.__description,
            "pic_url": self.__pic_url,
            "timestamp": self.__timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "id": str(self.__id),
        }
from internal.account import Account
from argon2 import PasswordHasher 
ph = PasswordHasher()

class Admin(Account):
    def __init__(self):
        username : str = "admin"
        password : str = "admin"
        super().__init__(username, ph.hash(password), "")
    
    def get_account_details(self) -> dict:
        return {
            "id": str(self.id),
            "username": self.username,
            "displayname":self.display_name,
            "role": "admin",
            "pic_url": self.pic_url,
            "timestamp": self.timestamp.strftime("%d/%m/%Y %H:%M:%S")
        }
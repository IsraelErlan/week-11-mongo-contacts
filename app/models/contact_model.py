from pydantic import BaseModel
from typing import Optional

class ContactObj:
    def __init__(self, first_name: str, last_name: str, phone_number: str, _id=None):
        self.id = str(_id) if _id else None
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def to_dict(self):
        if self.id:
            return {
                "_id": self.id, 
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number
            }
        else: 
            return {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number
            }
        


    @staticmethod
    def from_mongo(doc):
        return Contact(
            first_name=doc["first_name"],
            last_name=doc["last_name"],
            phone_number=doc["phone_number"],
            _id=doc["_id"]
        )




class Contact(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None







from models.contact_model import Contact, ContactObj
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError, ConnectionFailure

# import os

class DataInteractor:
    def __init__(self, db_name, collection_name):
        self.connection = None
        self.config = {"host": 'localhost',
                        "port": 27017
                        }
        self.db_name = db_name
        self.collection_name = collection_name


    def get_connection(self):
        if self.connection:
            return self.connection
        
        try: 
            self.connection = MongoClient(**self.config)
            return self.connection
        except:
            pass


    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except:
                pass


    def get_collection(self):
        try:
            conn = self.get_connection()
            db = conn[self.db_name]
            collection = db[self.collection_name]
            return collection
        except: 
            pass
        # finally: 
        #     self.close_connection()


    def phone_number_exist(self, collection, contact):
        is_exist = False if collection.count_documents({"phone_number": contact["phone_number"]}) == 0 else True
        return is_exist

    def create_contact(self, contact):
        try:
            collection = self.get_collection()
            if self.phone_number_exist(collection, contact):
                print(f"The phone number {contact['phone_number']} already exists!!!")
                return None
            result = collection.insert_one(contact)
            return str(result.inserted_id)
        except:
            pass


        
    def get_all_contacts(self):
        collection = self.get_collection()
        contacts = collection.find()
        result = [ContactObj.from_mongo(contact) for contact in contacts]
            
        return result
    




    def update_contact(self, contact_id: str, up_fields: dict):
        try:
            collection = self.get_collection()
            if "phone_number" in up_fields.keys() and self.phone_number_exist(collection, up_fields):
                print(f"The phone number {up_fields['phone_number']} already exists!!!")
                return None
            result = collection.update_one({'_id': ObjectId(contact_id)}, {"$set": up_fields})
            return result.matched_count > 0

        except:
            pass


    def delete_contact(self, contact_id: str) -> bool:
        collection = self.get_collection()
        try:
            result = collection.delete_one({"_id": ObjectId(contact_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Delete Error: {e}")
            return False
       
        




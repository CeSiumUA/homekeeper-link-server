from env import Env
import logging
from pymongo import MongoClient

class Database:

    __clients_collection_name = 'link-clients'
    __client_index_name = "client_id"

    def __init__(self) -> None:
        self.__connection_string = self.__get_connection_string()

    def get_client(self, client_id):
        collection = self.__get_clients_collection()
        return collection.find_one({self.__client_index_name: client_id})
    
    def get_overdue_clients(self, overdue_time):
        collection = self.__get_clients_collection()
        return collection.find({"last_online": {"$lt": overdue_time}, "notified": False})
    
    def update_client(self, client):
        collection = self.__get_clients_collection()
        collection.update_one({self.__client_index_name: client['client_id']}, {"$set": {"last_online": client['last_online'], "notified": client['notified']}})

    def add_client(self, client):
        collection = self.__get_clients_collection()
        collection.insert_one(client)

    def ensure_index_created(self):
        database = self.__get_database()
        collection = database[self.__clients_collection_name]
        if self.__client_index_name in collection.index_information():
            return
        
        collection.create_index(self.__client_index_name)

    def __enter__(self):
        self.__client = MongoClient(self.__connection_string)
        return self

    def __exit__(self, *args):
        self.__client.close()

    def __get_connection_string(self) -> str:
        cs = Env.get_mongo_srv()
        if cs is None:
            logging.fatal("connection string is empty")

        return cs
    
    def __get_database(self):
        return self.__client[Env.get_mongo_db()]
    
    def __get_clients_collection(self):
        db = self.__get_database()
        return db[self.__clients_collection_name]
import os
from pymongo import MongoClient

class Database:

    __clients_collection_name = 'link-clients'
    __client_index_name = "client_id"

    def __init__(self) -> None:
        self.__connection_string = self.__get_connection_string()

    def get_client(self, client_id):
        collection = self.__get_clients_collection()
        return collection.find_one({self.__client_index_name: client_id})

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
        return os.environ("MONGO_SRV")
    
    def __get_database(self):
        return self.__client[os.environ("MONGO_DB")]
    
    def __get_clients_collection(self):
        db = self.__get_database()
        return db[self.__clients_collection_name]
import database
import msgpack
import logging
from nacl.signing import VerifyKey

class Processor:
    def __init__(self, db: database.Database) -> None:
        self.__db = db

    def process(self, data):
        data = msgpack.unpackb(data)
        client = self.__db.get_client(data["client_id"])
        if client is None:
            return
        verify_key = VerifyKey(client["public_key"])
        time
        try:
            time = verify_key.verify(data["data"])
        except:
            logging.error("Wrong signature")
            return
        
        logging.info("Key verified")
        

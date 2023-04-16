import database
import msgpack
import logging
import time
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from env import Env
from notifier import TelegramNotifier
import asyncio

class Processor:
    def __init__(self, db: database.Database) -> None:
        self.__db = db

    def process(self, data):
        data = msgpack.unpackb(data)
        client = self.__db.get_client(data["client_id"])
        if client is None:
            return
        verify_key = VerifyKey(client["public_key"], encoder=HexEncoder)
        try:
            client_id = verify_key.verify(data["signature"], encoder=HexEncoder)
            client_id = str(client_id, 'utf-8')
            if client_id != client["client_id"]:
                raise ValueError
        except:
            logging.error("wrong signature")
            return
        
        logging.info("key verified")

        timestamp = time.time_ns()

        client['last_online'] = timestamp
        client['notified'] = False

        self.__db.update_client(client=client)

    def check_clients(self):
        overdue_time = time.time_ns() - Env.get_notify_interval_ns()

        clients = self.__db.get_overdue_clients(overdue_time=overdue_time)

        tl_token = Env.get_tl_token()

        if tl_token is None:
            logging.fatal("telegram bot token not provided")

        for client in clients:
            with TelegramNotifier(tl_token) as ntf:
                asyncio.run(ntf.send_text_message("Client ```{}``` is offline for more than 2 minutes".format(client["client_id"])))
            client["notified"] = True
            self.__db.update_client(client=client)
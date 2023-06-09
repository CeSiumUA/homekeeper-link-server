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

    KEEP_ALIVE_REQUEST = 0
    IP_ADDRESS_REQUEST = 1

    def __init__(self, db: database.Database) -> None:
        self.__db = db
        tl_token = Env.get_tl_token()

        if tl_token is None:
            logging.fatal("telegram bot token not provided")

        self.__ntf = TelegramNotifier(tl_token)

    def process(self, data, ep_ip) -> bytearray | None:
        data = msgpack.unpackb(data)
        if data['request_type'] == self.IP_ADDRESS_REQUEST:
            msg = {
                'ip_address': ep_ip
            }
            return msgpack.packb(msg)
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

        timestamp = int(time.time())

        if client['notified'] == True:
            client['notified'] = False
            asyncio.run(self.__ntf.send_text_message("Client `{}` is back online".format(client["display_name"])))

        if client['last_ip'] != ep_ip:
            client['last_ip'] = ep_ip
            asyncio.run(self.__ntf.send_text_message("Client `{}` has changed it's IP address to: `{}`".format(client["display_name"], client["last_ip"])))

        client['last_online'] = timestamp

        self.__db.update_client(client=client)

    def check_clients(self):
        overdue_time = int(time.time()) - Env.get_notify_interval()

        clients = self.__db.get_overdue_clients(overdue_time=overdue_time)

        for client in clients:
            asyncio.run(self.__ntf.send_text_message("Client `{}` is offline for more than 2 minutes".format(client["display_name"])))
            client["notified"] = True
            self.__db.update_client(client=client)
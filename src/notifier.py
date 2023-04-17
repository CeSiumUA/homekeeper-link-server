import telegram
from env import Env
import logging

class TelegramNotifier:
    def __init__(self, token) -> None:
        self.__token = token

    def __enter__(self):
        self.__bot = telegram.Bot(self.__token)
        return self

    async def send_text_message(self, message: str):
        chat_id = Env.get_chat_id()
        if chat_id is None:
            logging.fatal("chat id is not provided")
            return
        await self.__bot.send_message(chat_id=chat_id, text=message, parse_mode='MarkdownV2')

    def __exit__(self, *args):
        self.__bot.close()
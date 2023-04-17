import telegram
from env import Env
import logging

class TelegramNotifier:
    def __init__(self, token) -> None:
        self.__token = token

    async def send_text_message(self, message: str):
        bot = telegram.Bot(self.__token)
        chat_id = Env.get_chat_id()
        if chat_id is None:
            logging.fatal("chat id is not provided")
            return
        async with bot:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='MarkdownV2')
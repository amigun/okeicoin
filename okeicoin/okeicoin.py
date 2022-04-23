import configparser
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import handlers

config = configparser.ConfigParser()
config.read('../config.ini')

bot = Bot(token=config['Telegram']['bot_token'])
dp = Dispatcher(bot, storage=MemoryStorage())

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp)

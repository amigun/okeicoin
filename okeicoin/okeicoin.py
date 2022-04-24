import configparser
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
#from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import handlers

config = configparser.ConfigParser()
config.read('../config.ini')

bot = Bot(token=config['Telegram']['bot_token'])
#dp = Dispatcher(bot, storage=MemoryStorage())
dp = Dispatcher(bot, storage=RedisStorage2('127.0.0.1', 6379, db=5, pool_size=10, prefix='my_fsm_key'))

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp)

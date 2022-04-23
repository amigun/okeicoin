from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import messages

async def start(msg: types.Message, state: FSMContext):
    await msg.answer(messages.greeting)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

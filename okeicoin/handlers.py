from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import messages
import db_queries
import fsm

async def start(msg: types.Message, state: FSMContext):
    if db_queries.check_auth(msg.from_user.id) == msg.from_user.id:
        await msg.answer(messages.greeting)
    else:
        await msg.answer(messages.greeting_firsttime)

        await msg.answer(messages.enter_name)
        await fsm.AllStates.get_name.set()

async def get_name(msg: types.Message, state: FSMContext):
    await state.update_data(user_name=msg.text)

    await msg.answer(messages.enter_group)
    await fsm.AllStates.get_group.set()

async def get_group(msg: types.Message, state: FSMContext):
    await state.update_data(user_group=msg.text)

    user_data = await state.get_data()

    if db_queries.registration(msg.from_user.id, user_data['user_name'], user_data['user_group']) == 'success':
        await msg.answer(messages.success_registration)
    else:
        await msg.answer(messages.error_registration)

        await fsm.AllStates.main_menu.set()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(get_name, state=fsm.AllStates.get_name)
    dp.register_message_handler(get_group, state=fsm.AllStates.get_group)

import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import messages
import keyboards
import db_queries
import fsm

async def start(msg: types.Message, state: FSMContext):
    if db_queries.check_auth(msg.from_user.id) == msg.from_user.id:
        await msg.answer(messages.get['greeting'], reply_markup=keyboards.mainmenu__kb)
    else:
        await msg.answer(messages.get['greeting_firsttime'])

        await msg.answer(messages.get['enter_name'])
        await fsm.AllStates.get_name.set()

async def menu(msg: types.Message, state: FSMContext):
    if msg.text == messages.buttons['help']:
        await msg.answer(messages.get['help'])
    if msg.text == messages.buttons['profile']:
        await msg.answer(messages.get['profile'].format(*db_queries.get_info(msg.from_user.id)), parse_mode="MarkdownV2", reply_markup=keyboards.profile__kb)

async def profile_inline(call: types.CallbackQuery):
    if call.data == 'transfer':
        await call.message.answer(messages.get['not_enough_balance'])
    elif call.data == 'spend':
        if db_queries.get_balance(call.from_user.id) <= 0:
            await call.message.answer(messages.get['not_enough_balance'])
        else:
            await call.message.edit_text(messages.get['enter_count_of_coins'])
            
            await fsm.AllStates.enter_count_of_coins.set()

async def enter_count_of_coins(msg: types.Message, state: FSMContext):
    if (msg.text).isdigit():
        if int(msg.text) <= db_queries.get_balance(msg.from_user.id):
            db_queries.plus_balance(msg.from_user.id, -(int(msg.text)))

            await msg.answer(messages.get['success_of_withdraw'] + (datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
            
            await fsm.AllStates.main_menu.set()
        else:
            await msg.answer(messages.get['not_enough_balance'])
    else:
        await msg.answer(messages.get['isntdigit'])

async def get_name(msg: types.Message, state: FSMContext):
    await state.update_data(user_name=msg.text)

    await msg.answer(messages.get['enter_group'])
    await fsm.AllStates.get_group.set()

async def get_group(msg: types.Message, state: FSMContext):
    await state.update_data(user_group=msg.text)

    user_data = await state.get_data()

    if db_queries.registration(msg.from_user.id, user_data['user_name'], user_data['user_group']) == 'success':
        await msg.answer(messages.get['success_registration'], reply_markup=keyboards.mainmenu__kb)
        
        await fsm.AllStates.main_menu.set()
    else:
        await msg.answer(messages.get['error_registration'])

        await fsm.AllStates.main_menu.set()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(enter_count_of_coins, state=fsm.AllStates.enter_count_of_coins)
    dp.register_message_handler(get_name, state=fsm.AllStates.get_name)
    dp.register_message_handler(get_group, state=fsm.AllStates.get_group)
    dp.register_message_handler(menu, state='*')
    dp.register_callback_query_handler(profile_inline, lambda callback_query: True)

import datetime
import configparser
from aiogram import Bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import messages
import keyboards
import db_queries
import fsm

config = configparser.ConfigParser()
config.read('../config.ini')
bot = Bot(token=config['Telegram']['bot_token'])

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
        if db_queries.get_balance(call.from_user.id) <= 0:
            await call.message.answer(messages.get['not_enough_balance'])
        else:
            await call.message.edit_text(messages.get['enter_pay_account_to_transfer'])

            await fsm.AllStates.enter_pay_account_to_transfer.set()
    elif call.data == 'spend':
        if db_queries.get_balance(call.from_user.id) <= 0:
            await call.message.answer(messages.get['not_enough_balance'])
        else:
            await call.message.edit_text(messages.get['enter_count_of_coins'])
            
            await fsm.AllStates.enter_count_of_coins.set()

async def enter_pay_account_to_transfer(msg: types.Message, state: FSMContext):
    to_user_id = db_queries.check_pay_account(msg.text)
    if to_user_id is None:
        await msg.answer(messages.get['not_found_pay_account'])
    else:
        await state.update_data(to_user_id=to_user_id)
        await msg.answer(messages.get['enter_count_if_okeicoins'])

        await fsm.AllStates.enter_count_if_okeicoins.set()

async def enter_count_if_okeicoins(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()

    db_queries.plus_balance(msg.from_user.id, -(int(msg.text)))
    db_queries.plus_balance(user_data['to_user_id'], int(msg.text))

    await msg.answer(messages.get['you_transfer_okeicoins_to'])
    await bot.send_message(user_data['to_user_id'], messages.get['user_transfer_okeicoins_to_you'])

    await fsm.AllStates.main_menu.set()

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
    dp.register_message_handler(enter_pay_account_to_transfer, state=fsm.AllStates.enter_pay_account_to_transfer)
    dp.register_message_handler(enter_count_if_okeicoins, state=fsm.AllStates.enter_count_if_okeicoins)
    dp.register_message_handler(enter_count_of_coins, state=fsm.AllStates.enter_count_of_coins)
    dp.register_message_handler(get_name, state=fsm.AllStates.get_name)
    dp.register_message_handler(get_group, state=fsm.AllStates.get_group)
    dp.register_message_handler(menu, state='*')
    dp.register_callback_query_handler(profile_inline, lambda callback_query: True)

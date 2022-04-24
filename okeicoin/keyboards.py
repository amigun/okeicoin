from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import messages

mainmenu__kb = ReplyKeyboardMarkup(resize_keyboard=True)
mainmenu__kb.add(KeyboardButton(messages.buttons['help']),
        KeyboardButton(messages.buttons['profile']))

profile__kb = InlineKeyboardMarkup()
profile__kb.add(InlineKeyboardButton(text=messages.buttons['transfer'], callback_data='transfer'),
        InlineKeyboardButton(text=messages.buttons['spend'], callback_data='spend'))

from aiogram.types import KeyboardButton,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lexicon.lexicon import KEYBOARDS


def user_kb(state):
    if state == 'choice':
        kb_builder = ReplyKeyboardBuilder()
        btn = [KeyboardButton(text=f'{btn}') for btn in KEYBOARDS[state]]
        kb = kb_builder.row(*btn, width=2)
        return kb.as_markup(resize_keyboard = True, one_time_keyboard = True)

def user_inline_kb(state):
    i_kb_builder = InlineKeyboardBuilder()
    if state == 'todo':
        btn_edit = [InlineKeyboardButton(text=f'{KEYBOARDS["edit"][i]}', callback_data=f'{KEYBOARDS["edit"][i]}') for i in range(2)]
        i_kb_builder.row(*btn_edit, width=2)

    elif state == 'back':
        btn = [InlineKeyboardButton(text=KEYBOARDS['back'], callback_data='back')]
        i_kb_builder.row(*btn)
        return i_kb_builder.as_markup()
    else:
        btn_edit = [InlineKeyboardButton(text=KEYBOARDS['edit'][0], callback_data=KEYBOARDS['edit'][0])]
        i_kb_builder.row(*btn_edit, width=1)
    btn_pagination = [InlineKeyboardButton(text=f'{KEYBOARDS["edit"][i]}', callback_data=KEYBOARDS[KEYBOARDS["edit"][i]]) for i in range(2,4)]


    i_kb_builder.row(*btn_pagination, width=2)

    return i_kb_builder.as_markup()
from aiogram import Router

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, Text

from keyboards.user_keyboards import user_kb, user_inline_kb
from lexicon.lexicon import LEXICON
from filters.filters import USER_FSM, IsTask, IsDate, IsNote
from service.service import get_user_note, get_user_active_todo, get_user_finished_todo
from database import db


router = Router()
#Команда старт отправляет в чат клавиатуру с выбором действия
@router.message(CommandStart())
async def procces_command_start(message: Message):
    db.init_user(message.from_user.id)
    await message.answer(text=LEXICON['start'], reply_markup=user_kb('choice'))
    USER_FSM[message.from_user.id] = {'note': False, 'task': False, 'note_menu': [False, 0],
                                      'active_task': [False, 0], 'finished_task': [False, 0]}

#Команда help отправляет в чат справку с функциями бота
@router.message(Command(commands='help'))
async def add_todo(message: Message):
    await message.answer(text=LEXICON['help'])
    USER_FSM[message.from_user.id] = {'note': False, 'task': False,'note_menu': [False, 0],
                                      'active_task': [False, 0], 'finished_task': [False, 0]}

#Хендлер для добавления задачи
@router.message(Text(text='Добавить задачу'))
@router.message(Command(commands='addtodo'))
async def add_task(message: Message):
    await message.answer(text=LEXICON['task'], reply_markup=ReplyKeyboardRemove())
    USER_FSM[message.from_user.id] = {'note': False, 'task': True, 'note_menu': [False, 0],
                                      'active_task': [False, 0], 'finished_task': [False, 0]}


#Хендлер для добавления заметки
@router.message(Text(text='Добавить заметку'))
@router.message(Command(commands='addnote'))
async def add_note(message: Message):
    await message.answer(text=LEXICON['note'], reply_markup=ReplyKeyboardRemove())
    USER_FSM[message.from_user.id] = {'note': True, 'task': False, 'note_menu': [False, 0]}

#Проверка состояния юзера и добавления в массив его данных
@router.message(IsTask())
async def get_task(message: Message):
    await message.answer(text=LEXICON['date'])
    USER_FSM[message.from_user.id] = {'note': False, 'task': False, 'note_menu': [False, 0],
                                      'active_task': [False, 0], 'finished_task': [False, 0]}
    db.USER_INFO[message.from_user.id] = [message.from_user.id, message.from_user.full_name, message.text]

#Проверка состояния юзера и добавления даты в массив с его данными и INSERT в бд
@router.message(IsDate())
async def get_taks(message: Message):
    db.USER_INFO[message.from_user.id].append(message.text)
    db.insert_todo(db.USER_INFO[message.from_user.id][0], db.USER_INFO[message.from_user.id][1],db.USER_INFO[message.from_user.id][2], db.USER_INFO[message.from_user.id][3])
    await message.answer(text=LEXICON['todo_add'], reply_markup=user_kb('choice'))

#Проверка состояния юзера и INSERT его заметки в бд
@router.message(IsNote())
async def get_note(message: Message):
    db.insert_notes(message.from_user.id, message.from_user.full_name, message.text)
    USER_FSM[message.from_user.id] = {'note': False, 'task': False,'note_menu': [False, 0],
                                      'active_task': [False, 0], 'finished_task': [False, 0]}
    await message.answer(text=LEXICON['note_add'], reply_markup=user_kb('choice'))


#Команда для введения юзера в состояние просмотра заметок
#И отправки в чат его заметок
@router.message(Text(text='Мои заметки'))
@router.message(Command(commands='mynotes'))
async def show_note(message:Message):
    USER_FSM[message.from_user.id] = {'note': False, 'task': False, 'note_menu': [True, 0],
                                      'active_task': [False, 0], 'finished_task': [False, 0]}
    if get_user_note(message.from_user.id, USER_FSM[message.from_user.id]['note_menu'][1]):
        await message.answer(text=get_user_note(message.from_user.id, USER_FSM[message.from_user.id]['note_menu'][1]), reply_markup=user_inline_kb('note'))
    else:
        await message.answer(text='<b>У вас нет заметок</b>')

#Хендлер для перелистывания задач или заметок
@router.callback_query(Text(text='forward'))
async def pagination_procces(callback: CallbackQuery):
    if USER_FSM[callback.from_user.id]['note_menu'][0]:
        USER_FSM[callback.from_user.id]['note_menu'][1] += 1
        await callback.message.edit_text(text=get_user_note(callback.from_user.id, USER_FSM[callback.from_user.id]['note_menu'][1]), reply_markup=callback.message.reply_markup)
    elif USER_FSM[callback.from_user.id]['active_task'][0]:
        USER_FSM[callback.from_user.id]['active_task'][1] += 1
        await callback.message.edit_text(text=get_user_active_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['active_task'][1])[0], reply_markup=callback.message.reply_markup)
    elif USER_FSM[callback.from_user.id]['finished_task'][0]:
        USER_FSM[callback.from_user.id]['finished_task'][1] += 1
        await callback.message.edit_text(text=get_user_finished_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['finished_task'][1])[0], reply_markup=callback.message.reply_markup)

@router.callback_query(Text(text='backward'))
async def pagination_procces_backward(callback: CallbackQuery):
    if USER_FSM[callback.from_user.id]['note_menu'][0]:
        USER_FSM[callback.from_user.id]['note_menu'][1] -= 1
        await callback.message.edit_text(text=get_user_note(callback.from_user.id, USER_FSM[callback.from_user.id]['note_menu'][1]), reply_markup=callback.message.reply_markup)
    elif USER_FSM[callback.from_user.id]['active_task'][0]:
        USER_FSM[callback.from_user.id]['active_task'][1] -= 1
        await callback.message.edit_text(text=get_user_active_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['active_task'][1])[0], reply_markup=callback.message.reply_markup)
    elif USER_FSM[callback.from_user.id]['finished_task'][0]:
        USER_FSM[callback.from_user.id]['finished_task'][1] -= 1
        await callback.message.edit_text(text=get_user_finished_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['finished_task'][1])[0], reply_markup=callback.message.reply_markup)


#Хендлер для удаления задач или заметок
@router.callback_query(Text(text='Удалить'))
async def delete_user_entries(callback: CallbackQuery):
    if USER_FSM[callback.from_user.id]['note_menu'][0]:
        db.delete_notes(callback.from_user.id, callback.message.text)
        await callback.message.edit_text(text=LEXICON['delete'], reply_markup=user_inline_kb('back'))
    elif USER_FSM[callback.from_user.id]['active_task'][0]:
        db.delete_todo(callback.from_user.id, get_user_active_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['active_task'][1])[1])
        await callback.message.edit_text(text=LEXICON['delete'], reply_markup=user_inline_kb('back'))
    elif USER_FSM[callback.from_user.id]['finished_task'][0]:
        db.delete_todo(callback.from_user.id, get_user_finished_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['finished_task'][1])[1])
        await callback.message.edit_text(text=LEXICON['delete'], reply_markup=user_inline_kb('back'))

@router.callback_query(Text(text='Выполнено'))
async def completed_task(callback: CallbackQuery):
    db.update_todo(callback.from_user.id, get_user_active_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['active_task'][1])[1], True)
    await callback.message.edit_text(text=LEXICON['finished'], reply_markup=user_inline_kb('back'))

@router.callback_query(Text(text='back'))
async def procces_back_key(callback: CallbackQuery):
    if USER_FSM[callback.from_user.id]['note_menu'][0] and get_user_note(callback.from_user.id, USER_FSM[callback.from_user.id]['note_menu'][1]):
        await callback.message.edit_text(text=get_user_note(callback.from_user.id, USER_FSM[callback.from_user.id]['note_menu'][1])[0], reply_markup=user_inline_kb('todo+'))
    elif USER_FSM[callback.from_user.id]['active_task'][0] and get_user_active_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['active_task'][1]):
        await callback.message.edit_text(text=get_user_active_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['active_task'][1])[0], reply_markup=user_inline_kb('todo'))
    elif USER_FSM[callback.from_user.id]['finished_task'][0] and get_user_finished_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['finished_task'][1]):
        await callback.message.edit_text(text=get_user_finished_todo(callback.from_user.id, USER_FSM[callback.from_user.id]['finished_task'][1])[0], reply_markup=user_inline_kb('todo+'))
    else:
        await callback.message.edit_text(text=LEXICON['empty'])
        await callback.message.answer(text=LEXICON['empty_back'], reply_markup=user_kb('choice'))

@router.message(Text(text='Мои активные задачи'))
@router.message(Command(commands='activetask'))
async def show_finished_task(message: Message):
    USER_FSM[message.from_user.id] = {'note': False, 'task': False, 'task_menu': [False, 0], 'note_menu': [False, 0],
                                       'active_task': [True, 0], 'finished_task': [False, 0]}
    if get_user_active_todo(message.from_user.id, USER_FSM[message.from_user.id]['active_task'][1]):
        await message.answer(text=get_user_active_todo(message.from_user.id, USER_FSM[message.from_user.id]['active_task'][1])[0], reply_markup=user_inline_kb('todo'))
    else:
        await message.answer(text=LEXICON['empty'])

@router.message(Command(commands='finishedtask'))
async def show_finished_task(message: Message):
    USER_FSM[message.from_user.id] = {'note': False, 'task': False, 'task_menu': [False, 0],
                                      'note_menu': [False, 0], 'active_task': [False, 0], 'finished_task': [True, 0]}
    if get_user_finished_todo(message.from_user.id, USER_FSM[message.from_user.id]['finished_task'][1]):
        await message.answer(get_user_finished_todo(message.from_user.id, USER_FSM[message.from_user.id]['finished_task'][1])[0], reply_markup=user_inline_kb('todo+'))
    else:
        await message.answer(text=LEXICON['empty'])

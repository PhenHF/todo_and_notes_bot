from database import db
from filters.filters import USER_FSM

def get_user_note(user_id, count):
    notes = db.select_notes(user_id)
    if count <= len(notes) - 1 and count >= 0:
        return f'<b>{notes[count][0]}</b>'
    elif len(notes) == 0:
        return False
    else:
        count = 0
        USER_FSM[user_id]['note_menu'][1] = 0
        return f'<b>{notes[count][0]}</b>'

def get_user_active_todo(user_id, count):
    todo = db.select_active_todo(user_id)
    if count <= len(todo) - 1 and count >= 0:
        return [f'<b>{todo[count][0]}\n\nСтатус: Выполняется\n\n<u>{todo[count][1]}</u></b>', todo[count][0], len(todo)]
    elif len(todo) == 0:
        return False
    else:
        count = 0
        USER_FSM[user_id]['active_task'][1] = 0
        return [f'<b>{todo[count][0]}\n\nСтатус: Выполняется\n\n<u>{todo[count][1]}</u></b>', todo[count][0], len(todo)]

def get_user_finished_todo(user_id, count):
    todo = db.select_finished_todo(user_id)
    if count <= len(todo) - 1 and count >= 0:
        return [f'<b>{todo[count][0]}\n\nСтатус: Завершенно\n\n<u>{todo[count][1]}</u></b>', todo[count][0], len(todo)]
    elif len(todo) == 0:
        return False
    else:
        count = 0
        USER_FSM[user_id]['finished_task'][1] = 0
        return [f'<b>{todo[count][0]}\n\nСтатус: Завершенно\n\n<u>{todo[count][1]}</u></b>', todo[count][0], len(todo)]

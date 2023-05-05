import sqlite3

USER_INFO = {}

def sql_connection():
    con = sqlite3.connect('/home/tony/todo_and_notes_bot/database/Data.db')
    return con

def init_user(user_id):
    con = sql_connection()
    cur = con.cursor()

    check_user = cur.execute('SELECT * FROM user_id WHERE tg_user_id=?', (user_id,)).fetchall()
    if not check_user:
        cur.execute('INSERT INTO user_id(tg_user_id) VALUES(?)', (user_id,))
        con.commit()
        con.close()

def insert_notes(user_id, user_name, note):
    con = sql_connection()
    cur = con.cursor()

    cur.execute('INSERT INTO user_notes(tg_user_id, user_name, unotes) VALUES(?,?,?)', (user_id, user_name, note,))

    con.commit()
    con.close()

def insert_todo(user_id, user_name, todo, date):
    con = sql_connection()
    cur = con.cursor()

    cur.execute('INSERT INTO user_todo(tg_user_id, user_name, ToDo, user_date, status) VALUES(?,?,?,?,?)', (user_id, user_name, todo, date, False))

    con.commit()
    con.close()

def update_notes(user_id, note):
    con = sql_connection()
    cur = con.cursor()

    cur.execute('UPDATE user_notes SET unotes = ? WHERE tg_user_id = ?', (note, user_id))

    con.commit()
    con.close()

def update_todo(user_id, todo, status):
    con = sql_connection()
    cur = con.cursor()

    cur.execute('UPDATE user_todo set status = ? WHERE tg_user_id = ? and todo = ?', (status, user_id, todo))
    con.commit()
    con.close()

def select_notes(user_id):
    con = sql_connection()
    cur = con.cursor()

    user_info = cur.execute('SELECT unotes FROM user_notes WHERE tg_user_id = ?', (user_id,)).fetchall()
    con.close()
    return user_info

def select_todo(user_id):
    con = sql_connection()
    cur = con.cursor()

    user_info = cur.execute('SELECT ToDo, user_date, status FROM user_todo WHERE tg_user_id = ?', (user_id,)).fetchall()
    con.close()
    return user_info

def delete_notes(user_id, note):
    con = sql_connection()
    cur = con.cursor()

    cur.execute('DELETE FROM user_notes WHERE tg_user_id = ? and unotes = ?', (user_id, note))
    con.commit()
    con.close()

def delete_todo(user_id, todo):
    con = sql_connection()
    cur = con.cursor()

    cur.execute('DELETE FROM user_todo WHERE tg_user_id = ? and ToDo = ?', (user_id, todo))
    con.commit()

    con.close()

def select_active_todo(user_id):
    con = sql_connection()
    cur = con.cursor()

    user_info = cur.execute('SELECT ToDo, user_date, status FROM user_todo WHERE tg_user_id = ? and status = ?', (user_id, 0)).fetchall()
    con.close()
    return user_info

def select_finished_todo(user_id):
    con = sql_connection()
    cur = con.cursor()

    user_info = cur.execute('SELECT ToDo, user_date, status FROM user_todo WHERE tg_user_id = ? and status = ?', (user_id, 1)).fetchall()
    con.close()
    return user_info

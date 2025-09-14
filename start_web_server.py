from fastapi import FastAPI

import uvicorn

import sqlite3

import random
import string

"""
Данный код позволяет с помощью сайта создавать базу данных и добовлять данные о пользователе в неё.
"""
# Создаем приложение
app = FastAPI()


def gen_your_ss():
    characters = string.ascii_letters + string.digits
    your_s = ''.join(random.choice(characters) for _ in range(15))
    return your_s


@app.get("/pr_pols/phone_number={phone_number}")
def pr_pols(phone_number):
    con = sqlite3.connect('users.db')

    cursor = con.cursor()

    # Выполняем запрос COUNT(*)
    cursor.execute("SELECT COUNT(*) FROM user")

    # Получаем результат
    count = cursor.fetchone()[0]

    sp = []

    for i in range(1, count):
        con = sqlite3.connect('users.db')

        cursor = con.cursor()

        cursor.execute("SELECT phone_number FROM user WHERE id = ?",
                       (i,))

        # Используем fetchone(), чтобы получить одну запись
        row = cursor.fetchone()

        sp.append(row)

    if phone_number in sp:
        return False
    else:
        return True


@app.get("/pr_nik/nik={nik}")
def pr_pols_nik(nik):
    conn = sqlite3.connect(f'users.db')

    # Создание курсора
    cursor = conn.cursor()

    # Выполняем запрос COUNT(*)
    cursor.execute("SELECT COUNT(*) FROM user")

    # Получаем результат
    count = cursor.fetchone()[0]

    sp = []

    for i in range(1, count):
        con = sqlite3.connect('users.db')

        cursor = con.cursor()

        cursor.execute("SELECT nik FROM user WHERE id = ?",
                       (i,))

        # Используем fetchone(), чтобы получить одну запись
        row = cursor.fetchone()

        sp.append(row)

    if nik in sp:
        return False
    else:
        return True


# Обработчик маршрута "/"
@app.get("/")
async def send_message():
    return {
        "ok": True
    }


@app.get("/len_dan")
async def pr():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')

    # Создание курсора
    cursor = conn.cursor()

    # Выполняем запрос COUNT(*)
    cursor.execute("SELECT COUNT(*) FROM user")

    # Получаем результат
    count = cursor.fetchone()[0]

    # Закрываем подключение
    conn.close()

    return count


@app.get("/new_db")
async def create_gl_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Создаем таблицу 'users'
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number NOT NULL,
                nik NOT NULL,
                your_ss NOT NULL
            )
        ''')
    conn.close()
    return True


@app.get("/create_db/phone_number={phone_number}")
async def create_db(phone_number):
    conn = sqlite3.connect(f'users{phone_number}.db')
    cursor = conn.cursor()
    # Создаем таблицу 'users'
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number NOT NULL,
                nik NOT NULL,
                your_ss NOT NULL
            )
        ''')
    print("База данных создана успешно.")
    conn.close()
    return True


@app.get("/create_pols/name={name}/phone_number={phone_number}/nik={nik}")
async def create_pols(name, phone_number, nik):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    your_ss = gen_your_ss()
    cursor.execute(f'INSERT INTO user (name, phone_number, nik, your_ss) VALUES (?, ?, ?, ?)',
                   (name, phone_number, nik, your_ss))

    con = sqlite3.connect(f'users{phone_number}.db')
    cursor = con.cursor()
    try:
        cursor.execute(f'INSERT INTO user (name, phone_number, nik, your_ss) VALUES (?, ?, ?, ?)',
                       (name, phone_number, nik, your_ss))
        con.commit()
        # print(f"Пользователь {name} ({phone_number}) добавлен успешно.")
        return your_ss
    except sqlite3.IntegrityError as e:
        # print(f"Ошибка: {e}")
        return "error", e
    finally:
        con.close()


if __name__ == '__main__':
    uvicorn.run('start_web_server:app', reload=True, port=80)
    # !port=80!!!!!!!!!!!!!!!!!!


import config
from functions import final_count, buttons
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3 as sq
from datetime import datetime


class QuestionsState(StatesGroup):
    # Хранит на каком этапе диалога находится клиент
    GREETING = State()
    FIRST_QUESTIONS = State()
    SECOND_QUESTIONS = State()
    THIRD_QUESTIONS = State()
    FOURTH_QUESTIONS = State()
    FIFTH_QUESTIONS = State()
    FINISH = State()


bot = Bot(token=config.TELEGRAM_BOT_TOKEN, parse_mode='HTML')


# Создаем таблицу в базе данных sql
with sq.connect("baza_bot.db") as con:
    cur = con.cursor()
sql_request = """CREATE TABLE IF NOT EXISTS users (
    id TEXT NOT NULL,
    name TEXT,
    first_part INTEGER DEFAULT 0,
    nostalgist INTEGER DEFAULT 0,
    patriot INTEGER DEFAULT 0,
    antagonist INTEGER DEFAULT 0
)"""
con.execute(sql_request)

with sq.connect("baza_bot.db") as con:
    cur = con.cursor()
sql_request = """CREATE TABLE IF NOT EXISTS answer (
    id TEXT NOT NULL,
    name TEXT,
    answer TEXT,
    time INTEGER
)"""
con.execute(sql_request)


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
@dp.message_handler(state=QuestionsState.FINISH)
async def start_proccess(message: types.Message, state: FSMContext) -> None:
    msg = f"Привет {message.from_user.first_name} желаете пройти тест на вашу политическую принадлежность?"

    yes_btn = KeyboardButton('Да')
    no_btn = KeyboardButton('Нет')

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(yes_btn, no_btn)

    await message.answer(msg, reply_markup=markup)
    await state.set_state(QuestionsState.GREETING)


@dp.message_handler(state=QuestionsState.GREETING)
async def choose_restoraunts_process(message: types.Message, state: FSMContext):

    user_msg = message.text
    await state.update_data(FIRST=user_msg)

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    with sq.connect("baza_bot.db") as con:
        sql_request = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)"
    con.execute(sql_request, (user_id, user_name, 0, 0, 0, 0))
    con.commit()

    btn1, btn2, btn3, btn4 = buttons('Носил на груди', 'Приклеил огромную ленту к своей машине',
                                     'Не носил вообще', 'Выбросил в урну')

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer(f'Что бы вы делали с Георгиевской ленточкой на 9 мая?', reply_markup=markup)
    await state.set_state(QuestionsState.SECOND_QUESTIONS)


@dp.message_handler(state=QuestionsState.SECOND_QUESTIONS)
async def dish_process(message: types.Message, state: FSMContext):

    user_msg = message.text
    await state.update_data(SECOND=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Раньше такого не было', 'Это нормальная ситуация',
                                     'Россия наводнена мигрантами', 'Я не замечаю таких новостей')

    if user_msg == 'Носил на груди':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Приклеил огромную ленту к своей машине':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Не носил вообще':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Выбросил в урну':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Вы узнаете новость, что мигранты совершили преступление и остались безнаказанными.', reply_markup=markup)
    await state.set_state(QuestionsState.THIRD_QUESTIONS)


@dp.message_handler(state=QuestionsState.THIRD_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('ужасная инфляция', 'чертовы спекулянты',
                                     'зарплата так же не вырастет', 'за то нет войны!')

    if user_msg == 'Раньше такого не было':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Это нормальная ситуация':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Россия наводнена мигрантами':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Я не замечаю таких новостей':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Цены в пятерочке выросли на <b>20%</b>', reply_markup=markup)
    await state.set_state(QuestionsState.FOURTH_QUESTIONS)


@dp.message_handler(state=QuestionsState.FOURTH_QUESTIONS)
async def order_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(FOURTH=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Расстрелять', 'Корупция есть во всех странах',
                                     'Рыба гниет с головы', 'Нужно начать с себя')

    if user_msg == 'ужасная инфляция':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'чертовы спекулянты':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'зарплата так же не вырастет':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'за то нет войны!':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer("Вы узнаете новость, что очередной чиновник разворовывает страну", reply_markup=markup)
    await state.set_state(QuestionsState.FIFTH_QUESTIONS)


@dp.message_handler(state=QuestionsState.FIFTH_QUESTIONS)
async def finish_process(message: types.Message, state: FSMContext):
    user_msg = message.text

    await state.update_data(FINISH=user_msg)
    btn1 = KeyboardButton('Попробовать еще раз')

    if user_msg == 'Расстрелять':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    elif user_msg == 'Корупция есть во всех странах':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    elif user_msg == 'Рыба гниет с головы':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    elif user_msg == 'Нужно начать с себя':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    with sq.connect("baza_bot.db") as con:
        cur = con.cursor()
        user_id = message.from_user.id
    cur.execute(
        f"SELECT first_part, nostalgist, patriot, antagonist FROM users WHERE id = {user_id}")

    rows = cur.fetchall()
    rows2 = rows[0]
    first_part, nostalgist, patriot, antagonist = rows2

    result = final_count(first_part=first_part, nostalgist=nostalgist,
                         antagonist=antagonist, patriot=patriot)

    await message.answer(result)

    with sq.connect("baza_bot.db") as con:
        sql_request = "INSERT INTO answer VALUES(?, ?, ?, ?)"
        my_datetime = datetime(2222, 12, 10, 18, 10, 45)
        final_datetime = my_datetime.now()
        user_name = message.from_user.first_name
    con.execute(sql_request, (user_id, user_name, result, final_datetime))
    con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1)

    await message.answer("Желаете пройти еще раз?", reply_markup=markup)

    with sq.connect("baza_bot.db") as con:
        user_id = message.from_user.id
        sql_request = f"DELETE FROM users WHERE id = {user_id}"
    con.execute(sql_request)
    con.commit()
    await state.set_state(QuestionsState.FINISH)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

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
    SIXTH_QUESTIONS = State()
    SEVENTH_QUESTIONS = State()
    EIGHTH_QUESTIONS = State()
    NINTH_QUESTIONS = State()
    TENTH_QUESTIONS = State()
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

# приветствие


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

# первый вопрос


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

    btn1, btn2, btn3, btn4 = buttons('Я не замечал роста цен — неужели они так сильно выросли?', 'Цены растут в любом государстве, а в России рост стараются сдерживать.',
                                     'Раньше цены так не росли, виноваты спекулянты.', 'Вся система неэффективна — причина в плохих решениях, принимаемых десятилетиями.')

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer(f'Вы заходите в “Магнит” и замечаете, что цены на ходовые товары выросли в течение года. В чем причина происходящего?', reply_markup=markup)
    await state.set_state(QuestionsState.FIRST_QUESTIONS)


# второй вопрос
@dp.message_handler(state=QuestionsState.FIRST_QUESTIONS)
async def dish_process(message: types.Message, state: FSMContext):

    user_msg = message.text
    await state.update_data(SECOND=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Я не привык выражать свою позицию публично.', 'Носил бы на самом видном месте, в том числе наклеил на личный транспорте.',
                                     'Носил бы только на груди — как это и положено делать.', 'Не ношу ленточку — современная Россия не заслуживает чтить память о той войне.')

    if user_msg == 'Я не замечал роста цен — неужели они так сильно выросли?':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Цены растут в любом государстве, а в России рост стараются сдерживать.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Раньше цены так не росли, виноваты спекулянты.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Вся система неэффективна — причина в плохих решениях, принимаемых десятилетиями.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Что бы вы сделали с Георгиевской ленточкой на 9 мая?', reply_markup=markup)
    await state.set_state(QuestionsState.SECOND_QUESTIONS)


# третий вопрос
@dp.message_handler(state=QuestionsState.SECOND_QUESTIONS)
async def dish_process(message: types.Message, state: FSMContext):

    user_msg = message.text
    await state.update_data(SECOND=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Мигранты важны для экономики РФ. А преступления совершают все.', 'Россия страна многонациональная. Незачем делать акцент на нации.',
                                     'Причина в эксплуатации человека — мигрант бесправен и беден.', 'Миграция — проблема. Легкий путь решения властью государственных проблем.')

    if user_msg == 'Носил бы на самом видном месте, в том числе наклеил на личный транспорте.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Носил бы только на груди — как это и положено делать.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Я не привык выражать свою позицию публично.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Не ношу ленточку — современная Россия не заслуживает чтить память о той войне.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Вы услышали, что мигранты совершили чудовищное преступление:', reply_markup=markup)
    await state.set_state(QuestionsState.THIRD_QUESTIONS)

# четвертый вопрос


@dp.message_handler(state=QuestionsState.THIRD_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Пропаганда скрепляет общество.', 'Пропаганды в России нет — государственные СМИ так говорят во всем мире.',
                                     'Пропаганда в России есть, но лживая — в СССР хотя бы говорили правду.', 'Пропаганда в России есть и ее нужно запретить. Или дать мне, я скажу правду.')

    if user_msg == 'Россия страна многонациональная. Незачем делать акцент на нации.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Причина в эксплуатации человека — мигрант бесправен и беден.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Мигранты важны для экономики РФ. А преступления совершают все.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Миграция — проблема. Легкий путь решения властью государственных проблем.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('По телевизору в России все хорошо, а за рубежом очень плохо:', reply_markup=markup)
    await state.set_state(QuestionsState.FOURTH_QUESTIONS)

# пятый вопрос


@dp.message_handler(state=QuestionsState.FOURTH_QUESTIONS)
async def order_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(FOURTH=user_msg)

    btn1, btn2, btn3, btn4 = buttons('И зачем мне эта информация?', 'Лучше посчитайте сколько стоят бронированные автомобили президентов США.',
                                     'Стыдно. Сталин оставил после только китель, трубку, сапоги и 3 рубля денег', 'Расходы — урезать, все траты сделать прозрачнее.')

    if user_msg == 'Пропаганды в России нет — государственные СМИ так говорят во всем мире.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Пропаганда в России есть, но лживая — в СССР хотя бы говорили правду.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Пропаганда скрепляет общество.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Пропаганда в России есть и ее нужно запретить. Или дать мне, я скажу правду.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer("Один день жизни президента России обходится бюджету в 55 миллионов бюджетных денег:", reply_markup=markup)
    await state.set_state(QuestionsState.FIFTH_QUESTIONS)

# шестой вопрос


@dp.message_handler(state=QuestionsState.FIFTH_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Что-то такое слышал, но уже не помню.', 'В этом предложении меня расстраивает наречие «едва».',
                                     'А после улетел лечиться в Германию? Он точно наш?', 'Это преступление должно быть раскрыто, а виновные наказаны.')

    if user_msg == 'Лучше посчитайте сколько стоят бронированные автомобили президентов США.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Стыдно. Сталин оставил после только китель, трубку, сапоги и 3 рубля денег':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'И зачем мне эта информация?':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Расходы — урезать, все траты сделать прозрачнее.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Известный оппозиционер едва не умирает от отравления боевым веществом:', reply_markup=markup)
    await state.set_state(QuestionsState.SIXTH_QUESTIONS)

# седьмой вопрос


@dp.message_handler(state=QuestionsState.SIXTH_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Это очень разумно.', 'Медведев — кадровая ошибка. Это частное мнение неумного человека.',
                                     'Эти слова — роспись в бессилии системы.', 'В свободной стране с независимыми СМИ он бы уже подал в отставку.')

    if user_msg == 'В этом предложении меня расстраивает наречие «едва».':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'А после улетел лечиться в Германию? Он точно наш?':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Что-то такое слышал, но уже не помню.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Это преступление должно быть раскрыто, а виновные наказаны.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Высшее лицо государства считает, что работа учителем это призвание, а не заработок денег:', reply_markup=markup)
    await state.set_state(QuestionsState.SEVENTH_QUESTIONS)


# восьмой вопрос
@dp.message_handler(state=QuestionsState.SEVENTH_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Утечка мозгов проблема, но в теории решаемая.', 'Утечка мозгов проблема, но это активно решается.',
                                     'Утечка мозгов проблема, но никто это решать не хочет.', 'Утечка мозгов проблема, но лишь в череде сотен других проблем.')

    if user_msg == 'Медведев — кадровая ошибка. Это частное мнение неумного человека.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Эти слова — роспись в бессилии системы.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Это очень разумно.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'В свободной стране с независимыми СМИ он бы уже подал в отставку.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Россия каждый год выигрывает школьные олимпиады, но после все эти люди куда-то деваются?', reply_markup=markup)
    await state.set_state(QuestionsState.EIGHTH_QUESTIONS)


# девятый вопрос
@dp.message_handler(state=QuestionsState.EIGHTH_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Не хочешь, чтобы ремонтировали?', 'Делают и молодцы, чего жаловаться?',
                                     'Деньги легко украсть, а вот в СССР по безналу расчеты были.', 'Потому что коррупция — это системообразующий институт РФ.')

    if user_msg == 'Утечка мозгов проблема, но это активно решается.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Утечка мозгов проблема, но никто это решать не хочет.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Утечка мозгов проблема, но в теории решаемая.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Утечка мозгов проблема, но лишь в череде сотен других проблем.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Каждый год под моим окном ремонтируют одну и ту же дорогу?', reply_markup=markup)
    await state.set_state(QuestionsState.NINTH_QUESTIONS)


# десятый вопрос
@dp.message_handler(state=QuestionsState.NINTH_QUESTIONS)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(THIRD=user_msg)

    btn1, btn2, btn3, btn4 = buttons('Добился — молодец.', 'Он многого добился и теперь имеет право влиять на жизнь в своем регионе.',
                                     'Когда я услышу новость, что в Думу избран водитель такси?', 'Не новость, в Думе давно проходной двор.')

    if user_msg == 'Делают и молодцы, чего жаловаться?':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Деньги легко украсть, а вот в СССР по безналу расчеты были.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Не хочешь, чтобы ремонтировали?':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()
    elif user_msg == 'Потому что коррупция — это системообразующий институт РФ.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET antagonist = antagonist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(btn1, btn2, btn3, btn4)

    await message.answer('Трехкратный чемпион мира по боксу избран депутатом в Госдуму?', reply_markup=markup)
    await state.set_state(QuestionsState.TENTH_QUESTIONS)


# концовка
@dp.message_handler(state=QuestionsState.TENTH_QUESTIONS)
async def finish_process(message: types.Message, state: FSMContext):
    user_msg = message.text

    await state.update_data(FINISH=user_msg)
    btn1 = KeyboardButton('Попробовать еще раз')

    if user_msg == 'Он многого добился и теперь имеет право влиять на жизнь в своем регионе.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET patriot = patriot+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    elif user_msg == 'Когда я услышу новость, что в Думу избран водитель такси?':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET nostalgist = nostalgist+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    elif user_msg == 'Добился — молодец.':
        with sq.connect("baza_bot.db") as con:
            user_id = message.from_user.id
            sql_request = f"UPDATE users SET first_part = first_part+1 WHERE id = {user_id}"
            con.execute(sql_request)
            con.commit()

    elif user_msg == 'Не новость, в Думе давно проходной двор.':
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

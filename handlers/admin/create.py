from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.create_kb import place_kb, date_kb, time_kb
from state.create import CreateState
import os
import asyncpg


async def create_game(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберите площадку, где будет проходить игра',
                           reply_markup=place_kb())
    await state.set_state(CreateState.place)


async def select_place(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Место игры выбрано! \n'
                              f'Теперь выберите дату', reply_markup=date_kb())
    await state.update_data(place=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.date)


# ... (Остальные функции без изменений) ...

async def select_price(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Отлично, я записал игру')
    await state.update_data(price=message.text)
    create_data = await state.get_data()
    create_time = create_data.get('time').split('_')[1]

    # Подключение к базе данных PostgreSQL
    conn = await asyncpg.connect(
        user='ваш_пользователь',
        password='ваш_пароль',
        database='имя_вашей_базы_данных',
        host='хост',
        port='порт'
    )

    # Добавление игры в базу данных
    await conn.execute(
        'INSERT INTO ваша_таблица (place, date, time, minplayer, maxplayer, price) VALUES ($1, $2, $3, $4, $5, $6)',
        create_data['place'], create_data['date'], create_time, create_data['minplayer'], create_data['maxplayer'],
        create_data['price']
    )

    await conn.close()
    await state.clear()

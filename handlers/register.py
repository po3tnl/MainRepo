from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re
import os
import asyncpg

async def start_register(message: Message, state: FSMContext, bot: Bot):
    # Подключение к базе данных PostgreSQL
    conn = await asyncpg.connect(
        user='ваш_пользователь',
        password='ваш_пароль',
        database='имя_вашей_базы_данных',
        host='хост',
        port='порт'
    )

    # Выполнение запроса к базе данных
    users = await conn.fetch('SELECT * FROM users WHERE user_id = $1', message.from_user.id)

    if users:
        await bot.send_message(message.from_user.id, f'{users[0]["username"]} \n Вы уже зарегистрированы')
    else:
        await bot.send_message(message.from_user.id, f'Давайте начнем регистрацию. \n Скажите, как к вам можно обращаться? (имя фамилия)')
        await state.set_state(RegisterState.regName)

    # Закрытие соединения с базой данных
    await conn.close()

async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Приятно познакомиться, {message.text} \n'
                                                f'Теперь укажите номер телефона, чтобы быть на связи. \n'
                                                f'Формат телефона: +7XXXXXXXXXX \n\n'
                                                f'Внимание! Я чувствителен к формату')

    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)

async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if re.match(r'^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('regname')
        reg_phone = reg_data.get('regphone')
        msg = f'Приятно познакомиться, {reg_name} \n\n Ваш телефон: {reg_phone}'
        await bot.send_message(message.from_user.id, msg)

        # Подключение к базе данных PostgreSQL для добавления нового пользователя
        conn = await asyncpg.connect(
            user='ваш_пользователь',
            password='ваш_пароль',
            database='имя_вашей_базы_данных',
            host='хост',
            port='порт'
        )

        # Добавление пользователя в базу данных
        await conn.execute('INSERT INTO users (username, phone, user_id) VALUES ($1, $2, $3)', reg_name, reg_phone, message.from_user.id)

        # Закрытие соединения с базой данных
        await conn.close()

        await state.clear()
    else:
        await bot.send_message(message.from_user.id, f'Неправильный формат номера телефона. Пожалуйста, укажите номер в формате +7XXXXXXXXXX')

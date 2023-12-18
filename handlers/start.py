from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.profile_kb import profile_kb
import os
import asyncpg

async def get_start(message: Message, bot: Bot):
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
        await bot.send_message(message.from_user.id, f'Здравствуйте, {users[0]["username"]}!', reply_markup=profile_kb())
    else:
        await bot.send_message(message.from_user.id, '😊Вас приветствует Онлайн-Магазин Одежды\n'
                                                     '🐼Вы можете приобрести любую вещь из нашего Каталога\n'
                                                     'А также отслеживать Трэк-КОД приобретенного Товара👀\n\n\n',
                               reply_markup=register_keyboard())

    # Закрытие соединения с базой данных
    await conn.close()

async def get_help(message_help: Message, bot: Bot):
    await bot.send_message(message_help.from_user.id, 'Тут должна была быть какая-то инструкция '
                                                      'помощи, но мне лень, напишешь за меня? :)')

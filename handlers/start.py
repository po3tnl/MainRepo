from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.profile_kb import profile_kb
from utils.database import Database
import os


async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Здравствуйте {users[1]}! ', reply_markup=profile_kb())
    else:
        await bot.send_message(message.from_user.id, '😊Вас Приветсвует Онлайн-Магазин Одежды\n'
        '🐼Вы можете приобрести любую вещь из нашего Каталога\n'
        'А Также отслеживать Трэк-КОД приобретенного Товара👀\n\n\n', reply_markup=register_keyboard
    )

async def get_help(message_help: Message, bot: Bot):

    await bot.send_message(message_help.from_user.id, 'Тут должно была быть какая-та инструкция '
                                                      'помощи, но мне лень, напишешь за меня:)  ?')
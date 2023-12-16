from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.profile_kb import profile_kb
from utils.database import Database
import os


async def viewn_profile(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    games = db.db_select_column('games', 'status', 0)
    if (games):
        await bot.send_message(message.from_user.id, f'Актуальные игры:')
        for game in games:
            await bot.send_message(message.from_user.id, f'Игра состоится: {game[2]} в {game[3]} \n\n'
                                                         f'Минимальное число участников: {game[4]} \n\n'
                                                         f'Максимальное число участников: {game[5]} \n\n'
                                                         f'Стоимость игры: {game[6]}')
    else:
        await bot.send_message(message.from_user.id, f'В настоящее время игр пока не планируется')
from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.profile_kb import profile_kb
from utils.database import Database
import os
from keyboards.profile_kb import date_kb

async def viewn_game(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберите дату игры', reply_markup=date_kb())
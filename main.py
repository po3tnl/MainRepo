import asyncio
import os
from dotenv import load_dotenv
# https://www.youtube.com/watch?v=pVA8Hd8Zh68 ВОТ ВИДОС, СДЕЛАЙ ХОСТИНГ НА СЕРВЕР
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from utils.commands import set_commands
from handlers.start import get_start, get_help
from state.register import RegisterState
from state.create import CreateState
from handlers.register import start_register, register_name, register_phone
from handlers.admin.create import create_game, select_place, select_date, select_time, select_minplayer, select_maxplayer, select_price
from filters.CheckAdmin import CheckAdmin



load_dotenv()


token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()

async def start_bot(bot: Bot):
    await bot.send_message(5721135829, text='Я запустил бота')

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))
dp.message.register(get_help, Command(commands='help'))





# Регистрация Хендлера
dp.message.register(start_register, F.text=='Зарегистроваться в Магазине')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)
# Регистрируем хендлеры с созданием игры
dp.message.register(create_game, Command(commands='create'), CheckAdmin()) # Вместо игры, придумай что можно добавить в магазин
dp.callback_query.register(select_place, CreateState.place)
dp.callback_query.register(select_date, CreateState.date)
dp.callback_query.register(select_time, CreateState.time)
dp.message.register(select_minplayer, CreateState.minplayer)
dp.message.register(select_maxplayer, CreateState.maxplayer)
dp.message.register(select_price, CreateState.price)



async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())

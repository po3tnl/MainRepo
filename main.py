import asyncio
import os
import psycopg2
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from utils.commands import set_commands
from handlers.start import get_start, get_help
from state.register import RegisterState
from state.create import CreateState
from handlers.profile import viewn_profile
from handlers.register import start_register, register_name, register_phone
from handlers.admin.create import create_game, select_place, select_date, select_time, select_minplayer, select_maxplayer, select_price
from filters.CheckAdmin import CheckAdmin

load_dotenv()

# Получаем данные для подключения к PostgreSQL из переменных окружения
host = os.getenv('PG_HOST')
user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')
db_name = os.getenv('PG_DB_NAME')

try:
    # Подключение к базе данных PostgreSQL
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )

        print(f"Server version: {cursor.fetchone()}")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")

# Инициализация бота и диспетчера
token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')
bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot)


# Регистрация хэндлеров
async def start_bot(bot: Bot):
    await bot.send_message(5721135829, text='Я запустил бота')

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))
dp.message.register(get_help, Command(commands='help'))

dp.message.register(start_register, types.ContentTypes.TEXT, lambda message: message.text == 'Зарегистроваться в Магазине')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)

dp.message.register(create_game, Command(commands='create'), CheckAdmin())
dp.callback_query.register(select_place, CreateState.place)
dp.callback_query.register(select_date, CreateState.date)
dp.callback_query.register(select_time, CreateState.time)
dp.message.register(select_minplayer, CreateState.minplayer)
dp.message.register(select_maxplayer, CreateState.maxplayer)
dp.message.register(select_price, CreateState.price)

dp.message.register(viewn_profile, types.ContentTypes.TEXT, lambda message: message.text == 'Профиль')


# Запуск бота
async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())

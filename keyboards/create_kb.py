from aiogram.utils.keyboard import InlineKeyboardBuilder
import psycopg2
import os
import datetime
from utils.database import Database

def place_kb():
    db = Database('your_db_name', 'your_db_user', 'your_db_password', 'your_db_host', 'your_db_port')
    places = db.db_select_all('place')
    kb = InlineKeyboardBuilder()
    for place in places:
        kb.button(text=f'{place[1]}', callback_data=f'{place[0]}')
    kb.adjust(1)
    return kb.as_markup()

def date_kb():
    kb = InlineKeyboardBuilder()
    current_date = datetime.date.today()
    for i in range(7):
        current_date += datetime.timedelta(days=1)
        kb.button(text=f"{current_date.strftime('%d.%m')}", callback_data=f"{current_date.strftime('%d.%m.%y')}")
    kb.adjust(1)
    return kb.as_markup()

def time_kb():
    kb = InlineKeyboardBuilder()
    for x in range(9, 22, 3):
        kb.button(text=f"{x}:00", callback_data=f"time_{x}:00")
    kb.adjust(1)
    return kb.as_markup()
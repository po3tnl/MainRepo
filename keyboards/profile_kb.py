from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardBuilder
import datetime

def profile_kb():
    kb = ReplyKeyboardMarkup()
    kb.button(text="Актуальные игры")
    kb.button(text="Мои игры")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите действие')

def date_kb():
    kb = InlineKeyboardBuilder()
    current_date = datetime.date.today()
    for i in range(7):
        current_date += datetime.timedelta(days=1)
        kb.button(text=f"{current_date.strftime('%d.%m')}", callback_data=f"{current_date.strftime('%d.%m.%y')}")
    kb.adjust(1)
    return kb.as_markup()
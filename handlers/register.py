from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re
import os
from utils.database import Database

async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users): # Если Будет ошибка сделай так > if (users):
        await bot.send_message(message.from_user.id, f'{users[1]} \n Вы уже Зарегистрированы')
    else:
        await bot.send_message(message.from_user.id, f'Давайте Начнем Регистрацию \n Скажите Как к вам Можно обращаться? (имя фамилия)')
        await state.set_state(RegisterState.regName)



async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Приятно Познакомиться {message.text} \n'
                                                  f'Теперь Укажите Номер Телефона, чтобы быть на связи \n'
                                                  f'Формат Телефона +7XXXXXXXXXX \n\n'
                                                  f'Внимание! Я чувствителен к формату')

    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)



async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('regname')
        reg_phone = reg_data.get('regphone')
        msg = f'Приятно Познакомиться {reg_name} \n\n Ваш Телефон {reg_phone}'
        await bot.send_message(message.from_user.id, msg)
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_user(reg_name,reg_phone,message.from_user.id)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, f'Брат Номер не Правильный ты чето напутал')
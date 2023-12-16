from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.create_kb import place_kb, date_kb, time_kb

from state.create import CreateState
from utils.database import Database
import os

async def create_game(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберете площадку где будет проходить игра', reply_markup=place_kb())
    await state.set_state(CreateState.place)

async def select_place(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Место игры выбрано ! \n'
                              f'Дальше Выберите дату', reply_markup=date_kb())
    await state.update_data(place=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.date)

async def select_date(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Я успешно сохранил дату игры \n'
                              f'Выберете время игры', reply_markup=time_kb())
    await state.update_data(date=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.time)

async def select_time(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Укажите МИНИМАЛЬНОЕ количество игроков от 4 до 16')
    await state.update_data(time=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.minplayer)

async def select_minplayer(message: Message, state: FSMContext, bot: Bot):
    if(message.text.isdigit() and 4 <= int(message.text) <= 16):
        await bot.send_message(message.from_user.id, f'Хорошо, теперь укажите МАКСИМАЛЬНОЕ число игроков, значение должно быть от 4 до 16')
        await state.update_data(minplayer=message.text)
        await state.set_state(CreateState.maxplayer)
    else:
        await bot.send_message(message.from_user.id, 'Я ожидаю цифру от 4 до 16')

async def select_maxplayer(message: Message, state: FSMContext, bot: Bot):
    if(message.text.isdigit() and 4 <= int(message.text) <= 16):
        await bot.send_message(message.from_user.id, f'Теперь укажите стоимость игры') # в проект тз добавь, мол они раньше не имели возможности указывать разную сумму для разных людей
        await state.update_data(maxplayer=message.text)
        await state.set_state(CreateState.price)
    else:
        await bot.send_message(message.from_user.id, f'Я жду цифру от 4 до 16')

async def select_price(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Отлично, я Записал игру')
    await state.update_data(price=message.text)
    create_data = await state.get_data()
    create_time = create_data.get('time').split('_')[1]
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_game(create_data['place'], create_data['date'], create_time, create_data['minplayer'], create_data['maxplayer'], create_data['price'])
    await state.clear()
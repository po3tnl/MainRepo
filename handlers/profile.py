import asyncpg
import os


async def view_profile(message: Message, bot: Bot):
    # Подключение к базе данных PostgreSQL
    conn = await asyncpg.connect(
        user='ваш_пользователь',
        password='ваш_пароль',
        database='имя_вашей_базы_данных',
        host='хост',
        port='порт'
    )

    # Выполнение запроса к базе данных
    games = await conn.fetch('SELECT * FROM games WHERE status = $1', 0)

    if games:
        await bot.send_message(message.from_user.id, f'Актуальные игры:')
        for game in games:
            await bot.send_message(message.from_user.id, f'Игра состоится: {game["date"]} в {game["time"]} \n\n'
                                                         f'Минимальное число участников: {game["minplayer"]} \n\n'
                                                         f'Максимальное число участников: {game["maxplayer"]} \n\n'
                                                         f'Стоимость игры: {game["price"]}')
    else:
        await bot.send_message(message.from_user.id, f'В настоящее время игр пока не планируется')

    # Закрытие соединения с базой данных
    await conn.close()
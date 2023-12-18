from aiogram.filters import BaseFilter
from aiogram.types import Message
import os
from utils.database import Database

class CheckAdmin(BaseFilter):
    async def __call__(self, message: Message):
        try:
            admin_id = os.getenv('ADMIN_ID')
            db = Database('your_db_name', 'your_db_user', 'your_db_password', 'your_db_host', 'your_db_port')
            users = db.select_user_id(message.from_user.id)
            return users[3] in admin_id
        except:
            return False
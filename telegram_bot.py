from creat_bot import dp
from aiogram.utils import executor
from data_base import sqlite_db

async def on_start(_):
    sqlite_db.sql_start()

from handlers import client, admin, other

client.register_handlers_of_client(dp)
admin.register_handlers_of_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_start)
from aiogram import types, Dispatcher
from creat_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#ID = None
user_id = 941323228
class FSMAdmin(StatesGroup):
    product_id = State()
    category_id = State()
    photo = State()
    name = State()
    description = State()
    price = State()



#Получаем ID модератора
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    #global ID
    #ID = message.from_user.id
    if message.chat.id == user_id:
        await bot.send_message(message.chat.id, 'Что надо?', reply_markup=admin_kb.button_case_admin)
        #await message.delete()


async def cm_start(message: types.Message):
    if message.chat.id == user_id:
        await FSMAdmin.product_id.set()
        await message.answer('ID товара')

#Ловим первый ответ и пишим в словарь
async def load_product_id(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        async with state.proxy() as data:
            data['product_id'] = message.text
        await FSMAdmin.next()
        await message.answer('ID категории')

async def load_category_id(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        async with state.proxy() as data:
            data['category_id'] = message.text
        await FSMAdmin.next()
        await message.answer('Загрузи фото')

#@dp.message_handler(text='Загрузить', state=None)
"""async def cm_start(message: types.Message):
    if message.chat.id == user_id:
        await FSMAdmin.photo.set()
        await message.answer('Загрузи фото')"""

#Выход из состояний
#@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cansel(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        curent_state = await state.get_state()
        if curent_state is None:
            return
        await state.finish()
        await message.answer('OK')

#Ловим первый ответ и пишим в словарь
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.answer('Введи название')

#Ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.answer('Введи описание')

#Ловим треьий ответ
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.answer('Введи цену')

#Ловим четвертый ответ
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.chat.id == user_id:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await message.answer('Successfully')
        await state.finish()

#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callvack_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callvack_query.data.replace('del ', ''))
    await callvack_query.answer(text=f'{callvack_query.data.replace("del ", "")} удалена.', show_alert=True)

#@dp.message_handler(Text(equals='Удалить'))
async def delete_item(message: types.Message):
    if message.chat.id == user_id:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[2], f'ID<{ret[1]}>\n{ret[3]}\nОписание: {ret[4]}\nЦена: {ret[-1]}')
            await bot.send_message(message.chat.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                    add(InlineKeyboardButton(f'Удалить ID<{ret[1]}> {ret[3]}', callback_data=f'del {ret[3]}')))

#Регистрация хендлеров
def register_handlers_of_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, text=['Загрузить'], state=None)
    dp.register_message_handler(cansel, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_product_id, state=FSMAdmin.product_id)
    dp.register_message_handler(load_category_id, state=FSMAdmin.category_id)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, Text(equals='Удалить'))
from aiogram import types, Dispatcher
from keyboards import client_kb
from aiogram.dispatcher.filters import Text
from creat_bot import dp, bot
from data_base import sqlite_db
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, PreCheckoutQuery, ContentTypes
from config import pay_token
#class FSMClient(StatesGroup):

cb = CallbackData('btn', 'type', 'product_id', 'category_id')

async def gen_products(data, user_id):
    keyboard = InlineKeyboardMarkup()
    for i in data:
        count = await sqlite_db.get_count_in_cart(user_id, i[1])
        count = 0 if not count else sum(j[0] for j in count)

        keyboard.add(InlineKeyboardButton(text=f'В корзину📥: {i[5]}uzs x {count}шт',
                                          callback_data=f'btn:plus:{i[1]}:{i[6]}'))
        keyboard.add(InlineKeyboardButton(text='➖', callback_data=f'btn:minus:{i[1]}:{i[6]}'),
                     InlineKeyboardButton(text='➕', callback_data=f'btn:plus:{i[1]}:{i[6]}'),
                     InlineKeyboardButton(text='❌', callback_data=f'btn:del:{i[1]}:{i[6]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:-:-'))

    return keyboard

async def command_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}!   Добро пожаловать в DXShop!', reply_markup=client_kb.kb_client)
    try:
        await sqlite_db.add_users(message.chat.id, message.chat.first_name)
    except Exception as e:
        pass

#async def command_choosing_category(callback_query: types.CallbackQuery):
 #   await bot.send_message(callback_query.from_user.id, 'Выберите категорию:', reply_markup=client_kb.menu_kb_client)

#@dp.callback_query_handler(text='order1')
async def pizza_menu(message: types.Message):
    data = await sqlite_db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))

    await message.answer('Выберите категорию:', reply_markup=keyboard)
        #await bot.send_photo(message.from_user.id, i[2], f'ID<{i[1]}>\n{i[3]}\nОписание: {i[4]}\nЦена: {i[-1]}',
                             #reply_markup=keyboard)

        #"""await bot.send_photo(message.from_user.id, i[2], f'ID<{i[1]}>\n{i[3]}\nОписание: {i[4]}\nЦена: {i[-1]}',
        #                     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Заказать:{i[3]}',
        #                                                                                 callback_data=f'btn:buy:{i[1]}')))"""
        #await bot.send_message(message.chat.id, text='^^^', reply_markup=InlineKeyboardMarkup().
                           #    add(InlineKeyboardButton(text=f'Заказать:{i[3]}', callback_data=f'btn:buy:{i[1]}')))

@dp.callback_query_handler(cb.filter(type='category'))
async def goods(call: types.CallbackQuery, callback_data: dict):
    data = await sqlite_db.get_product(callback_data.get('category_id'))
    keyboard = await gen_products(data, call.message.chat.id)
    for i in data:
        await bot.send_photo(call.from_user.id, i[2], f'ID<{i[1]}>\n{i[3]}\nОписание: {i[4]}\nЦена: {i[-1]}',
                                      reply_markup=keyboard)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    #await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(cb.filter(type='back'))
async def back(call: types.CallbackQuery):
    data = await sqlite_db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))

    await bot.send_message(call.message.chat.id, text='Выберите категорию:', reply_markup=keyboard)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    #data = await sqlite_db.get_categories()
    #keyboard = InlineKeyboardMarkup()
    #for i in data:
    #    keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))

    #await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='minus'))
async def minus(call: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await sqlite_db.get_count_in_cart(call.message.chat.id, product_id)
    if not count_in_cart or count_in_cart[0][0] == 0:
        await call.message.answer('Товар отсуствует в корзине')
        return 0
    elif count_in_cart[0][0] == 1:
        await sqlite_db.remove_one_item(product_id, call.message.chat.id)
    else:
        await sqlite_db.change_count(count_in_cart[0][0] - 1, product_id, call.message.chat.id)

    data = await sqlite_db.get_product(callback_data.get('category_id'))
    keyboard = await gen_products(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='plus'))
async def plus(call: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_stock = await sqlite_db.get_count_in_stock(product_id)
    count_in_cart = await sqlite_db.get_count_in_cart(call.message.chat.id, product_id)
    if count_in_stock[0][0] == 0:
        await call.message.answer('Товара нет в наличии :(')
        return 0
    elif not count_in_cart or count_in_cart[0][0] ==0:
        await sqlite_db.add_to_cart(call.message.chat.id, call.message.chat.first_name, product_id)
        await call.answer('Добавил', show_alert=True)
    elif count_in_cart[0][0] < count_in_stock[0][0]:
        await sqlite_db.change_count(count_in_cart[0][0] + 1, product_id, call.message.chat.id)
    else:
        await call.message.answer('Больше нет в наличии')
        return 0

    data = await sqlite_db.get_product(callback_data.get('category_id'))
    keyboard = await gen_products(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='del'))
async def delete(call: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')

    count_in_cart = await sqlite_db.get_count_in_cart(call.message.chat.id,product_id)
    if not count_in_cart:
        await call.message.answer('Товар в корзине отвуствует')
        return 0
    else:
        await sqlite_db.remove_one_item(product_id, call.message.chat.id)

    data = await sqlite_db.get_product(callback_data.get('category_id'))
    keyboard = await gen_products(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

async def empty_cart(message: types.Message):
    await sqlite_db.empty_cart(message.chat.id)
    await message.answer('Корзина пуста!')


#@dp.callback_query_handler(cb.filter(type='buy'))
#async def add_to_cart(callback: types.CallbackQuery, callback_data: dict):
#    #await callback.answer(cache_time=10)
#
#    name = callback.message.chat.first_name
#    user_id = callback.message.chat.id
#    product_id = callback_data.get('id')
#
#    await sqlite_db.add_to_cart(user_id, name, product_id)
#
##    await callback.answer('Добавил', show_alert=True)

async def buy(message: types.Message):
    sss = await sqlite_db.get_count_in_cart1(message.chat.id)

    if not sss or sss[0][0] == 0:
        await message.answer('Корзина пуста!')
    else:
        data = await sqlite_db.get_cart(message.chat.id)
        new_data = []
        for i in range(len(data)):
            new_data.append(await sqlite_db.get_user_product(data[i][3]))
        new_data = [new_data[i][0] for i in range(len(new_data))]
        prices = [types.LabeledPrice(label=new_data[i][3]+f' x {data[i][4]}',
                                     amount=new_data[i][5]*100*data[i][4]) for i in range(len(new_data))]

        await bot.send_invoice(message.chat.id,
                               title='TEST',
                               description='ddd',
                               provider_token=pay_token,
                               currency='uzs',
                               prices=prices,
                               start_parameter='example',
                               payload='some_invoice')

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def s_pay(message: types.Message):
    await sqlite_db.empty_cart(message.chat.id)
    await bot.send_message(message.chat.id, 'Платеж прошел успешно')

#Регистрация хендлеров
def register_handlers_of_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(pizza_menu, Text(equals='🛒 Заказать'))
    dp.register_message_handler(empty_cart, Text(equals='🗑 Очистить корзину'))
    #dp.register_callback_query_handler(lambda x: x.data and x.data.startswith('order1'))
    #dp.register_callback_query_handler(cb.filter(type='order1'))
    #dp.register_callback_query_handler(command_pizza_selection, text='order1')
    dp.register_message_handler(buy, Text(equals='📥 Корзина'))
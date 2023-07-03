from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#ГЛАВНОЕ МЕНЮ
button1 = KeyboardButton('🛒 Заказать')
button2 = KeyboardButton('📥 Корзина')
button3 = KeyboardButton('🗑 Очистить корзину')
#button4 = KeyboardButton('ℹ️ О Компании')
#button5 = KeyboardButton('⚙️ Настройки')




kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(button1,button2).add(button3)


btn_menu_kb_client1 = KeyboardButton('Пицца')
btn_menu_kb_client2 = KeyboardButton('Бургер')
btn_menu_kb_client3 = KeyboardButton('Назад')
menu_kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb_client.row(btn_menu_kb_client1, btn_menu_kb_client2).add(btn_menu_kb_client3)


inline_kb_pizza = InlineKeyboardMarkup(row_width=2)
inline_kb_btn_client_pizza1 = InlineKeyboardButton('Пицца1', callback_data='order_pizza1')
inline_kb_btn_client_pizza2 = InlineKeyboardButton('Пицца2', callback_data='order_pizza2')
inline_kb_btn_client_pizza3 = InlineKeyboardButton('Пицца3', callback_data='order_pizza2')
inline_kb_btn_client_pizza4 = InlineKeyboardButton('Пицца4', callback_data='order_pizza2')
inline_kb_pizza.add(inline_kb_btn_client_pizza1, inline_kb_btn_client_pizza2, inline_kb_btn_client_pizza3, inline_kb_btn_client_pizza4)

inline_kb_burger = InlineKeyboardMarkup(row_width=2)
inline_kb_btn_client_burger1 = InlineKeyboardButton('Бургер1', callback_data='order_pizza1')
inline_kb_btn_client_burger2 = InlineKeyboardButton('Бургер2', callback_data='order_pizza2')
inline_kb_btn_client_burger3 = InlineKeyboardButton('Бургер3', callback_data='order_pizza2')
inline_kb_btn_client_burger4 = InlineKeyboardButton('Бургер4', callback_data='order_pizza2')
inline_kb_burger.add(inline_kb_btn_client_burger1, inline_kb_btn_client_burger2, inline_kb_btn_client_burger3, inline_kb_btn_client_burger4)

# МЕНЮ ЗАКАЗА
btn_num1 = KeyboardButton('1')
btn_num5 = KeyboardButton('5')
btn_num10 = KeyboardButton('10')
btn_num15 = KeyboardButton('15')
btn_num20 = KeyboardButton('20')

kb_client1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client1.row(btn_num1,btn_num5,btn_num10).add(btn_num15,btn_num20)
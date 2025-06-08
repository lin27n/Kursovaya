from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types

# Главное меню (Reply-клавиатура)
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="❓ Приемная комиссия КФУ"),
        types.KeyboardButton(text="🎓 Направления ИВМИиТ")
    )
    return builder.as_markup(resize_keyboard=True)

# Инлайн-кнопки для всех остальных случаев
def get_navigation_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")
    )
    return builder.as_markup()
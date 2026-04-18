from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup,KeyboardButton, ReplyKeyboardRemove
reply_kb = ReplyKeyboardMarkup (
 keyboard= [
     [
     KeyboardButton(text="список команд")
    ],

 ],
   resize_keyboard =True
)

full_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="список команд")],
        [
            KeyboardButton(text="Секретный чат"),
            KeyboardButton(text="Напоминание"),
        ],
        [
            KeyboardButton(text="секретарь"),
            KeyboardButton(text="таймер")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура без кнопки "список команд" - только основные функции
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Секретный чат"),
            KeyboardButton(text="Напоминание"),
        ],
        [
            KeyboardButton(text="секретарь"),
            KeyboardButton(text="таймер")
        ]
    ],
    resize_keyboard=True
)
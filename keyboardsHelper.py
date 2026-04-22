from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup,KeyboardButton, ReplyKeyboardRemove
reply_kb = ReplyKeyboardMarkup (
 keyboard= [
     [
     KeyboardButton(text="список команд")
    ],

 ],
   resize_keyboard =True
)
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
back_remind_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Напоминание")],
        
    ],
    resize_keyboard=True
)

secretary_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Потратить")],
    [KeyboardButton(text="Добавить доход")],
    [KeyboardButton(text="Установить цель")],
    [KeyboardButton(text= "История")],
    [KeyboardButton(text="Мой баланс")],
    [KeyboardButton(text="Назад")]
], resize_keyboard=True)
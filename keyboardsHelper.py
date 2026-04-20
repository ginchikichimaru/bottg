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
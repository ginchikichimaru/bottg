from aiogram import Bot, Dispatcher, Router, F
import asyncio 
import os
from dotenv import load_dotenv 
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart 
from reminder import reminderbuttons

router = Router()
load_dotenv()
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
   first_name = message.from_user.first_name
   last_name = message.from_user.last_name
   
   if last_name:
       name = f"{first_name} {last_name}"
   else:
       name = first_name
   
   await message.answer(f"Привет, {name}! Я - твой бот, который поможет тебе с различными задачами. Чем я могу помочь тебе сегодня? Напиши /help, чтобы узнать о моих возможностях.")
   
async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не сущ")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

@router.message(F.text == "/help")
async def cmd_help(message: Message) -> None:
    await message.answer("КОМАНДЫ:\n/start - начать общение с ботом\n/help - показать список команд\n/remind - взаимодействие с напоминаниями")

@router.message(F.text == "/remind")
async def callback_remind(message: Message) -> None:
    await message.answer("Выберите действие:", reply_markup=reminderbuttons.inline_kb)

if __name__ == "__main__":  
    asyncio.run(main())
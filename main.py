from aiogram import Bot, Dispatcher, Router
import asyncio 
import os
from dotenv import load_dotenv 
from aiogram.types import Message 
from aiogram.filters import CommandStart 

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
   
   await message.answer(f"Привет, {name}! Я - твой бот, который поможет тебе с различными задачами. Чем я могу помочь тебе сегодня?")
   
async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не установлен в переменных окружения")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":  
    asyncio.run(main())
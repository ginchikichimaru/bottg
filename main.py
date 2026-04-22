from aiogram import Bot, Dispatcher, Router, F
import asyncio 
import os
from dotenv import load_dotenv 
from keyboardsHelper import reply_kb, main_kb, back_remind_main
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup,KeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import CommandStart 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import router
from reminder import reminderbuttons 
import secretchat  
from database import SessionLocal, User
load_dotenv()

class BotStates(StatesGroup):
    waiting_for_action = State()
    help_message_sent = State()
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
   first_name = message.from_user.first_name
   last_name = message.from_user.last_name
   
   if last_name:
       name = f"{first_name} {last_name}"
   else:
       name = first_name
   
   db = SessionLocal()
   try:
       existing_user = db.query(User).filter(User.user_id == message.from_user.id).first()
       if not existing_user:
           new_user = User(
               user_id=message.from_user.id,
               username=message.from_user.username,
               first_name=message.from_user.first_name,
               last_name=message.from_user.last_name
           )
           db.add(new_user)
           db.commit()
   except Exception as e:
       db.rollback()
       print(f"Error saving user: {e}")
   finally:
       db.close()
   
   await message.answer(f"Привет, {name}! Я - твой бот, который поможет тебе с различными задачами. Чем я могу помочь тебе сегодня? Напиши /help или нажми на кнопку ниже.", reply_markup=reply_kb)
async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не сущ")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

@router.message(F.text.in_(["/help", "список команд"]))
async def cmd_help(message: Message, state: FSMContext) -> None:
    await message.delete()
    
    data = await state.get_data()
    if 'help_message_id' in data:
        try:
            await message.bot.delete_message(message.chat.id, data == ['help_message_id'])
        except:
            pass  
    
    sent_message = await message.answer("КОМАНДЫ:\n/remind - взаимодействие с напоминаниями \n/secretchat - отправить секретное сообщение\n/Secretary - калькулятор и счетчик финансов\n/timer - установить таймер", reply_markup=main_kb)
    await state.update_data(help_message_id=sent_message.message_id)
    await state.set_state(BotStates.help_message_sent)

@router.message(F.text.in_(["/remind", "Напоминание"]))
async def message_remind(message: Message, state: FSMContext) -> None:
    await message.delete()
    
    data = await state.get_data()
    if 'help_message_id' in data:
        try:
            await message.bot.delete_message(message.chat.id, data['help_message_id'])
        except:
            pass
        await state.update_data(help_message_id=None)
    
    await message.answer("Выберите действие:", reply_markup = reminderbuttons.inline_kb)
    photo = FSInputFile("/home/gin/bottg/photo/photo_2026-04-20_06-27-21.jpg")
    await message.answer_photo(photo=photo, reply_markup=reply_kb)
   


if __name__ == "__main__":  
    asyncio.run(main())
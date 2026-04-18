from aiogram import Bot, Dispatcher, Router, F
import asyncio 
import os
from dotenv import load_dotenv 
from keyboardsHelper import reply_kb, full_kb, main_kb
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup,KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import router
from reminder import reminderbuttons 
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
    
    # Удаляем предыдущее сообщение бота, если оно есть
    data = await state.get_data()
    if 'help_message_id' in data:
        try:
            await message.bot.delete_message(message.chat.id, data['help_message_id'])
        except:
            pass  # Сообщение уже могло быть удалено
    
    # Отправляем новое сообщение и сохраняем его ID
    sent_message = await message.answer("КОМАНДЫ:\n/remind - взаимодействие с напоминаниями \n/secretchat - отправить секретное сообщение\n/Secretary - калькулятор и счетчик финансов\n/timer - установить таймер", reply_markup=main_kb)
    await state.update_data(help_message_id=sent_message.message_id)
    await state.set_state(BotStates.help_message_sent)

@router.message(F.text == "/remind")
async def message_remind(message: Message, state: FSMContext) -> None:
    await message.delete()
    
    # Удаляем сообщение с командами, если оно есть
    data = await state.get_data()
    if 'help_message_id' in data:
        try:
            await message.bot.delete_message(message.chat.id, data['help_message_id'])
        except:
            pass
        await state.update_data(help_message_id=None)
    
    await message.answer("Выберите действие:", reply_markup=reminderbuttons.inline_kb)


if __name__ == "__main__":  
    asyncio.run(main())
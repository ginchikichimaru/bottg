from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import os
from keyboardsHelper import main_kb
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from config import router
from database import SessionLocal, SecretMessage, User

class SecretChatStates(StatesGroup):
    Waiting_for_user_id = State()
    Waiting_for_message = State()

@router.message(F.text.in_(["/secretchat", "Секретный чат"]))
async def cmd_secretchat(message: Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" Назад", callback_data="secret_chat_back")]
    ])
    await message.answer("Введите username (начиная с @) или Telegram ID получателя:", reply_markup=kb)
    await state.set_state(SecretChatStates.Waiting_for_user_id)

@router.message(SecretChatStates.Waiting_for_user_id)
async def process_user_id(message: Message, state: FSMContext):
    input_text = message.text.strip()
    to_user_id = None
    
    if input_text.startswith('@'):
        username = input_text[1:]  
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                to_user_id = user.user_id
            else:
                await message.answer(f"Пользователь @{username} не найден. Введите другой username или числовой ID:")
                return
        except Exception as e:
            await message.answer(f"Ошибка при поиске пользователя: {str(e)}\nПопробуйте ввести числовой ID:")
            return
        finally:
            db.close()
    else:
        try:
            to_user_id = int(input_text)
        except ValueError:
            await message.answer("Неверный формат. Введите @username или числовой ID.")
            return
    
    if to_user_id:
        await state.update_data(to_user_id=to_user_id)
        await message.answer("Теперь введите секретное сообщение:")
        await state.set_state(SecretChatStates.Waiting_for_message)

@router.message(SecretChatStates.Waiting_for_message)
async def process_secret_message(message: Message, state: FSMContext, bot: Bot):
    secret_text = message.text.strip()
    if not secret_text:
        await message.answer("Сообщение не может быть пустым!")
        return

    data = await state.get_data()
    to_user_id = data.get('to_user_id')

    # Сохранить в БД
    db = SessionLocal()
    try:
        new_message = SecretMessage(
            from_user_id=message.from_user.id,
            to_user_id=to_user_id,
            message=secret_text
        )
        db.add(new_message)
        db.commit()

        # Отправить сообщение
        try:
            await bot.send_message(chat_id=to_user_id, text=f"Секретное сообщение: {secret_text}")
            await message.answer("Секретное сообщение отправлено!")
        except Exception as e:
            await message.answer(f"Не удалось отправить сообщение: {str(e)}")
    except Exception as e:
        db.rollback()
        await message.answer(f"Ошибка сохранения: {str(e)}")
    finally:
        db.close()

    await state.clear()

@router.callback_query(F.data == "secret_chat_back")
async def secret_chat_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("КОМАНДЫ:\n/remind - взаимодействие с напоминаниями \n/secretchat - отправить секретное сообщение\n/Secretary - калькулятор и счетчик финансов\n/timer - установить таймер", reply_markup=main_kb)
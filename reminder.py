from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio 
import os
from keyboardsHelper import back_remind_main
from dotenv import load_dotenv 
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart 
from config import router
from database import SessionLocal, Reminder
import pytz 
class reminderStates(StatesGroup):
    Waiting_for_text = State()
    Waiting_for_delete_ids = State()

class reminderbuttons:
 inline_kb = InlineKeyboardMarkup(inline_keyboard=[
       [InlineKeyboardButton(text="Установить напоминание", callback_data="set_reminder")],
       [InlineKeyboardButton(text="Показать список напоминаний", callback_data="list_reminders")],
       [InlineKeyboardButton(text="Удалить напоминание", callback_data="delete_reminder")],
   ])

@router.callback_query(F.data == "set_reminder")
async def set_reminder_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer("Создаем заметку! Запишите ваш текст")
        await callback.answer()
        await state.set_state(reminderStates.Waiting_for_text)


@router.callback_query(F.data == "list_reminders")
async def list_reminders_callback(callback: CallbackQuery):
    if callback.message:
       user_id = callback.from_user.id
       db = SessionLocal()
       try:
           reminders = db.query(Reminder).filter(Reminder.user_id == user_id)
           if not reminders: 
             await callback.message.answer("У вас нет напоминаний :(", reply_markup=back_remind_main)
           else:
             answ = "Загружено, ваш список: \n\n"
             for i, reminder in enumerate(reminders, 1):
               moscow_tz = pytz.timezone('Europe/Moscow')
               local_time = reminder.created_at.replace(tzinfo=pytz.utc).astimezone(moscow_tz)
               answ += f"{i}. {reminder.text}\n"
               answ += f"   (Создано: {local_time.strftime('%d.%m.%Y %H:%M')})\n\n"           
           await callback.message.answer(answ)

       except Exception as ex:
         await callback.message.answer(f"Ошибка {str (ex)}")
       finally: db.close()
       
       await callback.answer()
@router.callback_query(F.data == "delete_reminder")
async def delete_reminder_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        user_id = callback.from_user.id
        db = SessionLocal()
        try:
            reminders = db.query(Reminder).filter(Reminder.user_id == user_id).all()
            
            if not reminders:
                await callback.message.answer("У вас нет напоминаний для удаления", reply_markup=back_remind_main)
            else:
                text = " Ваши напоминания (укажите номер для удаления):\n\n"
                for i, reminder in enumerate(reminders, 1):
                    text += f"{i}. {reminder.text}\n"
                
                text += "\n Напишите номера для удаления через пробел (например: 1 3 5)"
                await callback.message.answer(text)
                await state.set_state(reminderStates.Waiting_for_delete_ids)
                reminder_ids = [r.id for r in reminders]
                await state.update_data(reminder_ids=reminder_ids)
        except Exception as e:
            await callback.message.answer(f"Ошибка: {str(e)}")
        finally:
            db.close()
        
        await callback.answer()


@router.message(reminderStates.Waiting_for_text)
async def process_reminder_text(message: Message, state:FSMContext):
    reminder_text = message.text.strip()
    if not reminder_text:
        await message.answer("Текст не может быть пустым!")
        return
    
    db = SessionLocal()
    try:
        new_reminder = Reminder(user_id=message.from_user.id, text=reminder_text)
        db.add(new_reminder)
        db.commit()
        await message.answer(" Сохранено!", reply_markup=back_remind_main )
    except Exception as e:
        db.rollback()
        await message.answer(f" Ошибка: {str(e)}")
    finally:
        db.close()
    await state.clear()
    

@router.message(reminderStates.Waiting_for_delete_ids)
async def process_delete_reminder(message: Message, state: FSMContext):
    try:
        
        input_text = message.text.strip()
        numbers = input_text.split()
        
 
        data = await state.get_data()
        reminder_ids = data.get('reminder_ids', [])
        
     
        indices_to_delete = []
        for num in numbers:
            try:
                index = int(num) - 1
                if 0 <= index < len(reminder_ids):
                    indices_to_delete.append(index)
                else:
                    await message.answer(f"Номер {num} вне диапазона (1-{len(reminder_ids)})", reply_markup=back_remind_main)
            except ValueError:
                await message.answer(f" '{num}' не является числом", reply_markup=back_remind_main)
        
        if not indices_to_delete:
            await message.answer(" Не указаны корректные номера", reply_markup=back_remind_main)
            await state.clear()
            return
        
       
        db = SessionLocal()
        try:
            user_id = message.from_user.id
            deleted_count = 0
            
            for index in indices_to_delete:
                reminder_id = reminder_ids[index]
                db.query(Reminder).filter(
                    Reminder.id == reminder_id,
                    Reminder.user_id == user_id
                ).delete()
                deleted_count += 1
            
            db.commit()
            await message.answer(f"Удалено {deleted_count} напоминание(й)!", reply_markup=back_remind_main)
        except Exception as e:
            db.rollback()
            await message.answer(f" Ошибка удаления: {str(e)}")
        finally:
            db.close()
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
    
    await state.clear()
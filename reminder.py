from aiogram import Bot, Dispatcher, Router, F
import asyncio 
import os
from dotenv import load_dotenv 
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart 
from config import router
 
class reminderbuttons:
 inline_kb = InlineKeyboardMarkup(inline_keyboard=[
       [InlineKeyboardButton(text="Установить напоминание", callback_data="set_reminder")],
       [InlineKeyboardButton(text="Показать список напоминаний", callback_data="list_reminders")],
       [InlineKeyboardButton(text="Удалить напоминание", callback_data="delete_reminder")],
   ])

@router.callback_query(F.data == "set_reminder")
async def set_reminder_callback(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("Вы нажали кнопку!")
        await callback.answer()

@router.callback_query(F.data == "list_reminders")
async def list_reminders_callback(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("Вы нажали кнопку!")
        await callback.answer()

@router.callback_query(F.data == "delete_reminder")
async def delete_reminder_callback(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("Вы нажали кнопку!")
        await callback.answer()
from aiogram import Bot, Dispatcher, Router, F
import asyncio 
import os
from dotenv import load_dotenv 
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart 
from main import callback_remind
class reminderbuttons:
 inline_kb = InlineKeyboardMarkup(inline_keyboard=[
       [InlineKeyboardButton(text="Установить напоминание", callback_data="set_reminder")],
       [InlineKeyboardButton(text="Показать список напоминаний", callback_data="list_reminders")],
       [InlineKeyboardButton(text="Удалить напоминание", callback_data="delete_reminder")]
   ])
 
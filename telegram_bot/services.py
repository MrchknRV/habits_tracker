import asyncio
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .bot import bot


async def send_reminder(chat_id: int, text: str, habit_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выполнено ✅", callback_data=f"done_{habit_id}")]]
    )
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=keyboard)
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки напоминания: {e}")
        return False


def send_reminder_sync(chat_id: int, text: str, habit_id: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(send_reminder(chat_id, text, habit_id))
    finally:
        loop.close()

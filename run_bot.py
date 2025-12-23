import asyncio
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from telegram_bot.bot import bot, dp


async def main():
    print("Бот трекера привычек запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

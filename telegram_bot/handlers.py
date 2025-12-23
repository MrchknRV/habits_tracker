from aiogram import F, types
from aiogram.filters import Command, CommandStart
from asgiref.sync import sync_to_async

from habits.models import Habit
from users.models import User

from .bot import dp


@sync_to_async
def get_user_by_token(token_str: str):
    try:
        return User.objects.get(telegram_token=token_str)
    except User.DoesNotExist:
        return None


@sync_to_async
def save_user_chat_id(user, chat_id: int):
    user.telegram_chat_id = chat_id
    user.save(update_fields=["telegram_chat_id"])


@dp.message(CommandStart(deep_link=True))
async def cmd_start_with_link(message: types.Message):
    payload = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

    if payload.startswith("link_"):
        token_str = payload[5:]
        await process_link_token(message, token_str)
    else:
        await cmd_start(message)


@dp.message(Command("link"))
async def cmd_link(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "❌ Использование: /link <твой_токен>\n" "Пример: /link 22222222-2222-2222-2222-222222222222"
        )
        return

    token_str = args[1].strip()
    await process_link_token(message, token_str)


async def process_link_token(message: types.Message, token_str: str):
    user = await get_user_by_token(token_str)

    if not user:
        await message.answer("❌ Неверный или устаревший токен.\nПолучи новый в профиле на сайте.")
        return

    if user.telegram_chat_id is not None:
        await message.answer("❌ Этот аккаунт уже привязан к другому чату Telegram.")
        return

    await save_user_chat_id(user, message.chat.id)

    await message.answer(
        f"✅ Аккаунт успешно привязан!\n\n"
        f"<b>Email:</b> {user.email}\n"
        f"<b>Имя:</b> {user.get_full_name() or 'Не указано'}\n\n"
        f"Теперь ты будешь получать напоминания о привычках ⏰"
    )


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 <b>Привет! Это бот трекера привычек «Атомные привычки»</b>\n\n"
        "Чтобы получать напоминания:\n\n"
        "1. Зайди в профиль на сайте\n"
        "2. Получи токен\n"
        "3. Отправь мне:\n\n"
        "<code>/link твой_токен</code>\n\n"
        "Готово — напоминания придут вовремя!"
    )


@dp.callback_query(F.data.startswith("done_"))
async def callback_habit_done(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    try:
        habit = await sync_to_async(Habit.objects.get)(id=habit_id)
        if habit.user.telegram_chat_id != callback.message.chat.id:
            await callback.answer("Это не твоя привычка!", show_alert=True)
            return

        await callback.message.edit_text(
            callback.message.html_text + "\n\n✅ <b>Выполнено! Молодец!</b>", parse_mode="HTML"
        )
        await callback.answer("Отмечено как выполнено!")
    except Habit.DoesNotExist:
        await callback.answer("Привычка не найдена", show_alert=True)

from celery import shared_task
from django.utils import timezone

from telegram_bot.services import send_reminder_sync

from .models import Habit


@shared_task
def send_telegram_reminder(user_id: int, habit_id: int):
    try:
        habit = Habit.objects.select_related("user").get(id=habit_id, user_id=user_id)
        user = habit.user

        if not user.telegram_chat_id:
            return "Не привязан"

        message = (
            f"Пора выполнять привычку!\n\n"
            f"<b>{habit.action}</b>\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time.strftime('%H:%M')}\n"
            f"Длительность: {habit.execution_time} сек"
        )

        result = send_reminder_sync(user.telegram_chat_id, message, habit.id)
        return result

    except Exception as e:
        return str(e)


@shared_task
def check_and_send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time()

    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        time__hour=current_time.hour,
        time__minute__range=(current_time.minute + 5, current_time.minute - 5),
    ).select_related("user")

    sent = 0
    for habit in habits:
        if habit.last_sent:
            days_since = (now.date() - habit.last_sent.date()).days
            if days_since < habit.periodicity:
                continue

        send_telegram_reminder.delay(habit.user.id, habit.pk)
        habit.last_sent = timezone.now()
        habit.save(update_fields=["last_sent"])
        sent += 1

    print(f"Отправлено напоминаний: {sent}")

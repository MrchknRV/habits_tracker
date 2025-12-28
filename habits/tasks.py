from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder(user_id, habit_id):
    try:
        habit = Habit.objects.select_related("user").get(id=habit_id, user_id=user_id)
        user = habit.user

        if not user.telegram_chat_id:
            return "Telegram не привязан"

        message = (
            f"⏰ <b>Пора выполнять привычку!</b>\n\n"
            f"<b>Действие:</b> {habit.action}\n"
            f"<b>Место:</b> {habit.place}\n"
            f"<b>Время:</b> {habit.time.strftime('%H:%M')}\n"
            f"<b>Длительность:</b> {habit.execution_time} сек"
        )

        success = send_telegram_message(user.telegram_chat_id, message)
        return "Отправлено" if success else "Ошибка отправки"

    except Habit.DoesNotExist:
        return "Привычка не найдена"


@shared_task
def check_and_send_reminders():
    now = timezone.localtime()
    current_time = now.time()
    today = now.date()

    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        time__hour=current_time.hour,
        time__minute__range=(current_time.minute - 5, current_time.minute + 5),
    ).select_related("user")

    sent_count = 0
    for habit in habits:
        if habit.last_sent:
            days_since = (today - habit.last_sent.date()).days
            if days_since < habit.periodicity:
                continue

        send_habit_reminder.delay(habit.user.id, habit.pk)
        habit.last_sent = timezone.now()
        habit.save(update_fields=["last_sent"])
        sent_count += 1

    print(f"[Celery] Отправлено напоминаний: {sent_count}")
    return sent_count

from django.core.exceptions import ValidationError


def validate_habits(instance):
    if instance.is_pleasant:
        if instance.reward or instance.related_habit:
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

    if not instance.is_pleasant:
        if instance.reward and instance.related_habit:
            raise ValidationError("Одновременный выбор связанной привычки и указания вознаграждения не разрешен")

    if instance.related_habit and not instance.related_habit.is_pleasant:
        raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки")

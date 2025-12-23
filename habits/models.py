from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from habits.validators import validate_habits
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits", verbose_name="Пользователь")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=400, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная привычка",
    )
    reward = models.CharField(blank=True, null=True, verbose_name="Вознаграждение")
    periodicity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name="Периодичность"
    )
    execution_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)], verbose_name="Время на выполнения"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    last_sent = models.DateTimeField(null=True, blank=True, verbose_name="Последнее напоминание")

    def __str__(self):
        return f"{self.action} в {self.place} в {self.time}"

    class Meta:
        db_table = "habits"
        ordering = ["-time"]
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        validate_habits(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

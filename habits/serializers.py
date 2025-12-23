from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "reward",
            "periodicity",
            "execution_time",
            "is_public",
        ]
        read_only_fields = ["user", "id"]

    def validate(self, data):
        instance = Habit(**data)
        instance.user = self.context["request"].user

        try:
            instance.clean()
        except ValidationError as ex:
            raise ValidationError(ex.messages)

        return data

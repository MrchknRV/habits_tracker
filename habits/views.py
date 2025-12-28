from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPageNumberPagination
from habits.permissions import IsOwner, IsPublicOrOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = (IsPublicOrOwner,)
    pagination_class = HabitPageNumberPagination


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )
    pagination_class = HabitPageNumberPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

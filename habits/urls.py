from django.urls import path

from . import views

app_name = "habits"

urlpatterns = [
    path("habits/", views.PublicHabitListAPIView.as_view(), name="public-list"),
    path("habits/create/", views.HabitCreateAPIView.as_view(), name="create"),
    path("habits/mylist/", views.HabitListAPIView.as_view(), name="my-list"),
    path("habits/<int:pk>/", views.HabitRetrieveUpdateDestroyAPIView.as_view(), name="habit-detail-destroy"),
]

from django.urls import path

from . import views

app_name = "habits"

urlpatterns = [
    path("", views.PublicHabitListAPIView.as_view(), name="public-list"),
    path("create/", views.HabitCreateAPIView.as_view(), name="create"),
    path("mylist/", views.HabitListAPIView.as_view(), name="my-list"),
    path("<int:pk>/", views.HabitRetrieveUpdateDestroyAPIView.as_view(), name="habit-detail-destroy"),
]

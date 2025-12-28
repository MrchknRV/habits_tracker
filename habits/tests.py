from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()

class HabitTestCase(APITestCase):
    def setUp(self):
        # Создаём пользователей
        self.user1 = User.objects.create_user(email="user1@example.com", password="pass123456")
        self.user2 = User.objects.create_user(email="user2@example.com", password="pass123456")

        # Публичная привычка
        Habit.objects.create(
            user=self.user2,
            place="Парк",
            time="18:00:00",
            action="Бегать",
            is_public=True,
            execution_time=60,
            periodicity=1
        )

        # Приватная привычка user1
        self.private_habit = Habit.objects.create(
            user=self.user1,
            place="Дома",
            time="07:00:00",
            action="Зарядка",
            is_public=False,
            execution_time=120,
            periodicity=1
        )

    def test_create_habit(self):
        self.client.force_authenticate(self.user1)
        url = reverse('habits:create')
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Читать книгу",
            "execution_time": 60,
            "periodicity": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_list_my_habits(self):
        self.client.force_authenticate(self.user1)
        url = reverse('habits:my-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # только своя

    def test_list_public_habits(self):
        # Не авторизован — должен видеть публичные
        url = reverse('habits:public-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # только публичная

    def test_update_own_habit(self):
        self.client.force_authenticate(self.user1)
        url = reverse('habits:habit-detail-destroy', args=[self.private_habit.id])
        data = {"action": "Новая зарядка"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.private_habit.refresh_from_db()
        self.assertEqual(self.private_habit.action, "Новая зарядка")

    def test_cannot_update_foreign_habit(self):
        self.client.force_authenticate(self.user1)
        foreign_habit = Habit.objects.exclude(user=self.user1).first()
        url = reverse('habits:habit-detail-destroy', args=[foreign_habit.id])
        response = self.client.patch(url, {"action": "Хак"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # или 403

    def test_delete_own_habit(self):
        self.client.force_authenticate(self.user1)
        url = reverse('habits:habit-detail-destroy', args=[self.private_habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.private_habit.id).exists())
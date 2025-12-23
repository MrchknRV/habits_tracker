from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = "users"


urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("telegram/link/", views.GetTelegramTokenView.as_view(), name="telegram_link"),
]

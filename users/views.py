from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": user.email}, status=status.HTTP_201_CREATED)


class GetTelegramTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.user.telegram_token
        link = f"https://t.me/habitstracker_trainbot?start=link_{token}"
        return Response(
            {"token": str(token), "bot_link": link, "message": "Отправь боту команду: /link " + str(token)}
        )

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class UserManager(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'пользователь не авторизован'
        return Response({'username': username})

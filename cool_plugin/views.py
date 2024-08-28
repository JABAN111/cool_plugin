from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response


class UserManager(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'пользователь не авторизован'
        return Response({'username': username,})

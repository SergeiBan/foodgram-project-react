from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, ListUserSerializer
from core.pagination import CustomizedPagination


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = CustomizedPagination
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer()
    queryset = User.objects.all()

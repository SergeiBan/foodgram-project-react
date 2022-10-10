from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, ListUserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer()
    queryset = User.objects.all()

    # def get_serializer_class(self):
    #     print(self.action)
    #     if self.action == 'list':
    #         return ListUserSerializer
    #     else:
    #         return super().get_serializer_class()

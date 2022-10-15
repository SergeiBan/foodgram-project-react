from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, ListUserSerializer, SubscriptionSerializer
from core.pagination import CustomizedPagination
from rest_framework.response import Response


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = CustomizedPagination
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer()
    queryset = User.objects.all()


class SubscriptionViewSet(viewsets.ModelViewSet):
    pagination_class = CustomizedPagination
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer

    def list(self, request):
        subscriptions = request.user.subscriptions.all()
        serializer = self.serializer_class(subscriptions, many=True)
        return Response(serializer.data)
    


    

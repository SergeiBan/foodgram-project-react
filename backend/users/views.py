from rest_framework import viewsets, permissions, mixins, exceptions, status
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, ListUserSerializer, SubscriptionSerializer
from core.pagination import CustomizedPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Subscribe


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = CustomizedPagination
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer()
    queryset = User.objects.all()


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class SubscriptionViewSet(ListViewSet):
    pagination_class = CustomizedPagination
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()


class CreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class SubscribeUnsubscribeViewSet(CreateDeleteViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        id = self.request.kwargs.get('id')
        user = get_object_or_404(User, pk=id)
        return user.authors.all()

    def create(self, request, id):
        try:
            author = get_object_or_404(User, pk=id)
            Subscribe.objects.create(subscriber=request.user, author=author)
        except Exception as error:
            raise exceptions.ValidationError(error)
        
        serializer = self.get_serializer(author)
        return Response(serializer.data)
    
    def delete(self, request, id):
        try:
            author = get_object_or_404(User, pk=id)
            Subscribe.objects.get(subscriber=request.user, author=author).delete()
        except Exception as error:
            raise exceptions.ValidationError(error)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    

from rest_framework import status
from django.contrib.auth import get_user_model
from users.serializers import SubscriptionSerializer
from core.pagination import CustomizedPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Subscribe
from users.mixins import ListViewSet, CreateDeleteViewSet
from users.serializers import SubscribeSerializer


User = get_user_model()


class SubscriptionViewSet(ListViewSet):
    """
    Возвращает список подписок пользователя.
    """
    pagination_class = CustomizedPagination
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber=self.request.user)


class SubscribeUnsubscribeViewSet(CreateDeleteViewSet):
    """
    Создает и удаляет подписку.
    """
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        id = self.request.kwargs.get('id')
        user = get_object_or_404(User, pk=id)
        return user.authors.all()

    def create(self, request, id):
        serializer = self.get_serializer(
            data=request.data, context={'id': id, 'request': request})
        serializer.is_valid(raise_exception=True)
        author = get_object_or_404(User, pk=id)
        Subscribe.objects.create(subscriber=request.user, author=author)
        serializer = SubscriptionSerializer(
            author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        serializer = self.get_serializer(
            data=request.data, context={'id': id, 'request': request})
        serializer.is_valid(raise_exception=True)
        author = get_object_or_404(User, pk=id)
        Subscribe.objects.get(
            subscriber=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

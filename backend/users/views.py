from rest_framework import viewsets, mixins, exceptions, status
from django.contrib.auth import get_user_model
from users.serializers import SubscriptionSerializer
from core.pagination import CustomizedPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Subscribe


User = get_user_model()


class RetrieveListCreateViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class SubscriptionViewSet(ListViewSet):
    """
    Возвращает список подписок пользователя.
    """
    pagination_class = CustomizedPagination
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber=self.request.user)


class CreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class SubscribeUnsubscribeViewSet(CreateDeleteViewSet):
    """
    Создает и удаляет подписку.
    """
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        try:
            author = get_object_or_404(User, pk=id)
            Subscribe.objects.get(
                subscriber=request.user, author=author).delete()
        except Exception as error:
            raise exceptions.ValidationError(error)

        return Response(status=status.HTTP_204_NO_CONTENT)

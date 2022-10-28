from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe


User = get_user_model()


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ()

    def validate(self, attrs):
        id = self.context['id']

        if not User.objects.filter(pk=id).exists():
            raise exceptions.ValidationError('Такого автора нет.')

        user = self.context['user']
        author = User.objects.get(pk=id)
        if user == author:
            raise exceptions.ValidationError('Нельзя подписаться на себя.')

        return attrs

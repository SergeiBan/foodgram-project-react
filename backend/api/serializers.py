import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from recipes.models import Recipe
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64, base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    author = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'image', 'text', 'image', 'ingredients', 'tags',
            'cooking_time')

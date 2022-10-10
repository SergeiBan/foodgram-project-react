from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import TokenSerializer

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ('email', 'id', 'username', 'first_name', 'last_name')

# class ListUserSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = (
#             'email', 'id', 'username', 'first_name', 'last_name',
#             'is_subscribed')
        
#         def get_is_subscribed(self, obj):
#             user = self.context['request'].user
#             return obj in user.subscriptions.all()

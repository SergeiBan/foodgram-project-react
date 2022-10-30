from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('Логин', max_length=150, unique=True)
    password = models.CharField('Пароль', max_length=150)
    email = models.EmailField('Почта', max_length=254)
    last_name = models.CharField('Фамилия', max_length=150)
    first_name = models.CharField('Имя', max_length=150)

    class Meta:
        models.indexes = [
            models.Index(fields=['username'])
        ]


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User, verbose_name='Подписчик', on_delete=models.SET_NULL, null=True,
        related_name='authors')
    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.SET_NULL, null=True,
        related_name='subscribers')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='subscribe_subscriber_author_constraint'),

            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='no_self_subscribing')
        ]

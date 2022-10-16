from django.db import models
from django.contrib.auth.models import AbstractUser
# from recipes.models import Favorite



ROLES = (
    ('user', 'user'),
    ('admin', 'admin')
)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    role = models.CharField(max_length=6, choices=ROLES)
    subscriptions = models.ManyToManyField(
        'self', related_name='subs', blank=True, symmetrical=False)


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='authors')
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='subscribers')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='subscribe_subscriber_author_constraint')
        ]
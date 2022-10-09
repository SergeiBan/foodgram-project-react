from django.db import models
from django.contrib.auth.models import AbstractUser


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
    role = models.CharField(max_length=6, choices=ROLES)

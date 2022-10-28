from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Adds users to DB'

    def handle(self, *args, **kwargs):

        User.objects.create_user(
            username='a',
            password='A12341234',
            email='a@a.ru',
            first_name='a',
            last_name='a'),

        User.objects.create_user(
            username='b',
            password='B12341234',
            email='b@b.ru',
            first_name='b',
            last_name='b'
        ),

        User.objects.create_user(
            username='c',
            password='C12341234',
            email='c@c.ru',
            first_name='c',
            last_name='c')

        User.objects.create_user(
            username='superu',
            password='superpass',
            email='s@s.ru',
            first_name='s',
            last_name='s',
            is_staff=True,
            is_superuser=True)

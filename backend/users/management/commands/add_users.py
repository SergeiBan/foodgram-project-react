from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Adds users to DB'

    def handle(self, *args, **kwargs):

        User.objects.create_user(
            username='first',
            password='A12341234',
            email='a@a.ru',
            first_name='Афанасий',
            last_name='Никитин'),

        User.objects.create_user(
            username='second',
            password='B12341234',
            email='b@b.ru',
            first_name='Емельян',
            last_name='Пугачёв'
        ),

        User.objects.create_user(
            username='third',
            password='C12341234',
            email='c@c.ru',
            first_name='Евгений',
            last_name='Петросян')

        User.objects.create_user(
            username='superu',
            password='superpass',
            email='s@s.ru',
            first_name='Муслим',
            last_name='Магомаев',
            is_staff=True,
            is_superuser=True)

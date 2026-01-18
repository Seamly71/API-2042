from django.db import models
from django.contrib.auth.models import AbstractUser

from users.constants import MAX_LOGIN_LENGTH


class User(AbstractUser):

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

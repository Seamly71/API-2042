from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from geomessages.constants import TEXT_CUTOFF


User = get_user_model()


class Point(models.Model):
    point = models.PointField(
        geography=True,
        verbose_name='Точка'
    )

    class Meta:
        verbose_name = 'точка'
        verbose_name_plural = 'Точки'

    def __str__(self):
        return f'{self.point.coords[0]}, {self.point.coords[1]}'


class Message(models.Model):
    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        verbose_name='Точка',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField()

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.author.username}: {self.text[:TEXT_CUTOFF]}'

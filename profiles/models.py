# profiles/models.py

from django.conf import settings
from django.db import models
from workplace.models import Workplace


class Profile(models.Model):
    '''user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name = "Псевдоним"
    )'''
    bio = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="ФИО"
    )
    position=models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="Должность"
    )

    workplace = models.ForeignKey(
        Workplace,
        on_delete=models.CASCADE,
        verbose_name="рабочее место",
        null = True
    )


    def __str__(self):
        return self.bio

#
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профиль'

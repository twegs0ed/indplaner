from django.conf import settings
from django.db import models

class Workplace(models.Model):
    name = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="Наименование"

    )
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    class Meta:
        verbose_name = 'Место хранения'
        verbose_name_plural = 'Место хранения'
    def __str__(self):
        return self.name
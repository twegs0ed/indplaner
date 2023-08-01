from django.conf import settings
from django.db import models

class Workplace(models.Model):
    name = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="наименование"

    )
    machine = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="оборудование"
    )
    class Meta:
        verbose_name = 'рабочее место'
        verbose_name_plural = 'рабочее место'
    def __str__(self):
        return self.name
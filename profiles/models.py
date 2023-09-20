# profiles/models.py

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    #workplace = models.ForeignKey(
        #Workplace,
        #on_delete=models.CASCADE,
       # verbose_name="рабочее место",
       # null = True
   # )


    def __str__(self):
        return self.bio

#
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профиль'


class Operation(models.Model):
    name=models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="Название"
    )
    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операция'

class StanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="Операция", null=True, blank=True)
    class Meta:
        verbose_name = 'Станочники'
        verbose_name_plural = 'Станочники'
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StanProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.stanprofile.save()
    

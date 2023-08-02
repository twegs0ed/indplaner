# Generated by Django 3.2.9 on 2021-11-23 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'профиль', 'verbose_name_plural': 'профиль'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='ФИО'),
        ),
    ]
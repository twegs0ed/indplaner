# Generated by Django 3.2.9 on 2024-04-27 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0012_alter_work_ready'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='work_time',
            field=models.IntegerField(default=0, verbose_name='Время выполнения одной детали, мин'),
        ),
    ]

# Generated by Django 3.2.9 on 2023-08-29 07:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20230829_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firm',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата запуска'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date_worker',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата запуска'),
        ),
    ]

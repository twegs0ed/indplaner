# Generated by Django 3.2.9 on 2023-08-29 07:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_order_date_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_worker',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата запуска'),
        ),
    ]

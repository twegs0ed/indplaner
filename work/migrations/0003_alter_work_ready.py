# Generated by Django 3.2.9 on 2023-09-20 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_work_ready'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='ready',
            field=models.BooleanField(default=True, verbose_name='Деталь готова?'),
        ),
    ]

# Generated by Django 3.2.9 on 2023-09-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='ready',
            field=models.BooleanField(default=0, verbose_name='Деталь готова?'),
        ),
    ]

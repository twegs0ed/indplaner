# Generated by Django 3.2.9 on 2023-10-24 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0008_work_machines'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='machines',
        ),
    ]

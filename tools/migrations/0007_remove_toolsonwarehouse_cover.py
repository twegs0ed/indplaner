# Generated by Django 3.2.9 on 2023-09-27 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0006_toolsonwarehouse_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolsonwarehouse',
            name='cover',
        ),
    ]

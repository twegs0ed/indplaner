# Generated by Django 3.2.9 on 2021-11-29 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0010_auto_20211129_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolsonwarehouse',
            name='need_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Дефицит'),
        ),
    ]
# Generated by Django 3.2.9 on 2021-12-15 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0012_auto_20211201_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tools',
            name='count',
            field=models.IntegerField(null=True, verbose_name='Кол-во'),
        ),
    ]
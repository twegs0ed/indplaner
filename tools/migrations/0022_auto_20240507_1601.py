# Generated by Django 3.2.9 on 2024-05-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0021_auto_20240507_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='norms',
            name='eroz0',
            field=models.IntegerField(null=True, verbose_name='эроз 0 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz1',
            field=models.IntegerField(null=True, verbose_name='эроз 1 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz2',
            field=models.IntegerField(null=True, verbose_name='эроз 2 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz3',
            field=models.IntegerField(null=True, verbose_name='эроз 3 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz4',
            field=models.IntegerField(null=True, verbose_name='эроз 4 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz5',
            field=models.IntegerField(null=True, verbose_name='эроз 5 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz6',
            field=models.IntegerField(null=True, verbose_name='эроз 6 уст.'),
        ),
        migrations.AlterField(
            model_name='norms',
            name='eroz7',
            field=models.IntegerField(null=True, verbose_name='эроз 7 уст.'),
        ),
    ]
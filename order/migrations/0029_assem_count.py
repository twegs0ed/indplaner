# Generated by Django 3.2.9 on 2024-04-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_auto_20240402_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='assem',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во'),
        ),
    ]
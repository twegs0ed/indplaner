# Generated by Django 3.2.9 on 2024-07-24 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0017_workoptim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoptim',
            name='tool',
        ),
        migrations.AlterField(
            model_name='workoptim',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Предложение'),
        ),
    ]

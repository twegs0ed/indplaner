# Generated by Django 3.2.9 on 2023-08-01 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0017_alter_toolsonwarehouse_count'),
        ('order', '0006_auto_20230801_2314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Детали по изделиям', 'verbose_name_plural': 'Детали по изделиям'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('OW', 'В запуске'), ('OR', 'запущено'), ('PD', 'на стороне'), ('CM', 'изготовлено')], default='OW', editable=False, max_length=2, verbose_name='статус'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='tool',
        ),
        migrations.AddField(
            model_name='order',
            name='tool',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.toolsonwarehouse', verbose_name='Деталь'),
        ),
        migrations.AlterField(
            model_name='orderformed',
            name='status',
            field=models.CharField(choices=[('OW', 'В запуске'), ('OR', 'запущено'), ('PD', 'на стороне'), ('CM', 'изготовлено')], default='OW', max_length=2, verbose_name='статус'),
        ),
    ]
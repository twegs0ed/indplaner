# Generated by Django 3.2.9 on 2023-09-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_alter_toolsonwarehouse_workplace'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolsonwarehouse',
            name='count_in_one_stock',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Кол-во деталей из одной заготовки'),
        ),
        migrations.AddField(
            model_name='toolsonwarehouse',
            name='material',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Материал'),
        ),
        migrations.AddField(
            model_name='toolsonwarehouse',
            name='stock_sizes',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Габариты заготовки'),
        ),
    ]

# Generated by Django 3.2.9 on 2023-09-12 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_auto_20230912_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsonwarehouse',
            name='material',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Материал'),
        ),
    ]

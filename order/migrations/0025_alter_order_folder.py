# Generated by Django 3.2.9 on 2024-03-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_order_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='folder',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='pdf'),
        ),
    ]
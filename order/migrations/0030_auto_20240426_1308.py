# Generated by Django 3.2.9 on 2024-04-26 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0029_assem_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='firm',
            name='report',
            field=models.BooleanField(default=False, verbose_name='Для расчетов'),
        ),
        migrations.AlterField(
            model_name='firm',
            name='assem',
            field=models.ManyToManyField(blank=True, null=True, to='order.Assem', verbose_name='Сборки'),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-15 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20211201_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='firm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.firm', verbose_name='Поставщик'),
        ),
        migrations.AlterField(
            model_name='orderformed',
            name='status',
            field=models.CharField(choices=[('OW', 'Заявка'), ('OR', 'Заказан'), ('PD', 'Оплачен'), ('CM', 'Получено')], default='OW', max_length=2, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='orderformed',
            name='tools',
            field=models.ManyToManyField(blank=True, null=True, to='order.Order', verbose_name='Инструменты'),
        ),
    ]

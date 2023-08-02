# Generated by Django 3.2.9 on 2021-12-01 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0011_toolsonwarehouse_need_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tools',
            name='count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Кол-во'),
        ),
        migrations.AlterField(
            model_name='toolsonwarehouse',
            name='period',
            field=models.CharField(choices=[('LGP', 'Долгий срок'), ('SHP', 'Расходник')], default='SHP', max_length=3, verbose_name='Срок эксплуатации'),
        ),
    ]
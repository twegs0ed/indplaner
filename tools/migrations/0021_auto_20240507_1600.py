# Generated by Django 3.2.9 on 2024-05-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0020_auto_20240507_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='norms',
            name='eroz0',
            field=models.IntegerField(null=True, verbose_name="эроз'. ун. 0 уст."),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz1',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 1 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz2',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 2 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz3',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 3 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz4',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 4 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz5',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 5 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz6',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 6 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='eroz7',
            field=models.IntegerField(null=True, verbose_name='эроз. ун. 7 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='lentopil',
            field=models.IntegerField(null=True, verbose_name='пила'),
        ),
    ]

# Generated by Django 3.2.9 on 2024-05-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0019_auto_20240507_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='norms',
            name='mill0',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 0 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill1',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 1 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill2',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 2 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill3',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 3 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill4',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 4 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill5',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 5 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill6',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 6 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='mill7',
            field=models.IntegerField(null=True, verbose_name='фрез. ун. 7 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn0',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 0 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn1',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 1 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn2',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 2 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn3',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 3 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn4',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 4 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn5',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 5 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn6',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 6 уст.'),
        ),
        migrations.AddField(
            model_name='norms',
            name='turn7',
            field=models.IntegerField(null=True, verbose_name='ток. ун. 7 уст.'),
        ),
    ]
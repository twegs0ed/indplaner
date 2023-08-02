# Generated by Django 3.2.9 on 2023-08-02 12:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workplace', '__first__'),
        ('profiles', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toolsonwarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Обозначение')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата получения на склад')),
                ('count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество на складе')),
                ('workplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workplace.workplace', verbose_name='Место хранения')),
            ],
            options={
                'verbose_name': 'Детали',
                'verbose_name_plural': 'Детали на складе',
            },
        ),
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('count', models.IntegerField(default=0, null=True, verbose_name='Кол-во')),
                ('giveout_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата выдачи')),
                ('tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.toolsonwarehouse', verbose_name='Деталь')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Работник')),
            ],
            options={
                'verbose_name': 'Выдача',
                'verbose_name_plural': 'Выдача деталей',
            },
        ),
        migrations.CreateModel(
            name='Rec_Tools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('count', models.IntegerField(null=True, verbose_name='Кол-во')),
                ('giveout_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата сдачи')),
                ('tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.toolsonwarehouse', verbose_name='Деталь')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Работник')),
            ],
            options={
                'verbose_name': 'Брак',
                'verbose_name_plural': 'Отбракованные детали',
            },
        ),
        migrations.CreateModel(
            name='Priem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(null=True, verbose_name='Кол-во')),
                ('giveout_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата приема')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workplace.workplace', verbose_name='Место хранения')),
                ('tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.toolsonwarehouse', verbose_name='Детали')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Работник, от которого принята деталь')),
            ],
            options={
                'verbose_name': 'прием',
                'verbose_name_plural': 'прием деталей на склад',
            },
        ),
    ]

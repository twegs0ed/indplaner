# Generated by Django 3.2.9 on 2023-09-20 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=160, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операция',
            },
        ),
        migrations.CreateModel(
            name='StanProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.operation', verbose_name='Операция')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Станочники',
                'verbose_name_plural': 'Станочники',
            },
        ),
    ]

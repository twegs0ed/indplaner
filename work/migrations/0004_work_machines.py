# Generated by Django 3.2.9 on 2023-09-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20230920_1107'),
        ('work', '0003_alter_work_ready'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='machines',
            field=models.ManyToManyField(to='profiles.Machine'),
        ),
    ]

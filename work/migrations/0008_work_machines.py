# Generated by Django 3.2.9 on 2023-10-02 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20230920_1107'),
        ('work', '0007_remove_work_machines'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='machines',
            field=models.ManyToManyField(blank=True, null=True, to='profiles.Machine', verbose_name='Станки'),
        ),
    ]

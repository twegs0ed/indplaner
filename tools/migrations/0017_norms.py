# Generated by Django 3.2.9 on 2024-05-07 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0016_alter_toolsonwarehouse_similar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Norms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnctun1', models.IntegerField(null=True, verbose_name='ток. чпу 1 уст.')),
                ('cnctun2', models.IntegerField(null=True, verbose_name='ток. чпу 2 уст.')),
                ('cnctun3', models.IntegerField(null=True, verbose_name='ток. чпу 3 уст.')),
                ('cnctun4', models.IntegerField(null=True, verbose_name='ток. чпу 4 уст.')),
                ('cnctun5', models.IntegerField(null=True, verbose_name='ток. чпу 5 уст.')),
                ('cnctun6', models.IntegerField(null=True, verbose_name='ток. чпу 6 уст.')),
                ('cnctun7', models.IntegerField(null=True, verbose_name='ток. чпу 7 уст.')),
                ('cncmill1', models.IntegerField(null=True, verbose_name='фрез. чпу 1 уст.')),
                ('cncmill2', models.IntegerField(null=True, verbose_name='фрез. чпу 2 уст.')),
                ('cncmill3', models.IntegerField(null=True, verbose_name='фрез. чпу 3 уст.')),
                ('cncmill4', models.IntegerField(null=True, verbose_name='фрез. чпу 4 уст.')),
                ('cncmill5', models.IntegerField(null=True, verbose_name='фрез. чпу 5 уст.')),
                ('cncmill6', models.IntegerField(null=True, verbose_name='фрез. чпу 6 уст.')),
                ('cncmill7', models.IntegerField(null=True, verbose_name='фрез. чпу 7 уст.')),
                ('tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.toolsonwarehouse', verbose_name='Деталь')),
            ],
            options={
                'verbose_name': 'Нормы времени',
                'verbose_name_plural': 'Нормы времени',
            },
        ),
    ]

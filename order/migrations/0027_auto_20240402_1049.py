# Generated by Django 3.2.9 on 2024-04-02 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0016_alter_toolsonwarehouse_similar'),
        ('order', '0026_firm_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='firm',
            name='assem_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во сборок в изд.'),
        ),
        migrations.CreateModel(
            name='Assem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Сборочный узел')),
                ('tool_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('tool', models.ManyToManyField(null=True, to='tools.Toolsonwarehouse', verbose_name='Детали')),
            ],
            options={
                'verbose_name': 'Сборочные узлы',
                'verbose_name_plural': 'Сборочные узлы',
            },
        ),
        migrations.AddField(
            model_name='firm',
            name='assem',
            field=models.ManyToManyField(null=True, to='order.Assem', verbose_name='Сборки'),
        ),
    ]
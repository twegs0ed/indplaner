# Generated by Django 3.2.9 on 2023-09-20 12:14

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_firm_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='firm',
            name='color2',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=[('#FFFFFF', 'white'), ('#000000', 'black')]),
        ),
    ]

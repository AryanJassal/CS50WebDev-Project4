# Generated by Django 3.1 on 2020-11-07 04:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 7, 15, 2, 41, 427341), editable=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 7, 15, 2, 41, 426344), editable=False),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-31 10:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betterLife', '0009_poruka_procitana'),
    ]

    operations = [
        migrations.AddField(
            model_name='poruka',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
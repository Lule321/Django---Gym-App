# Generated by Django 4.0.4 on 2022-05-31 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betterLife', '0008_alter_razgovor_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='poruka',
            name='procitana',
            field=models.BooleanField(default=True),
        ),
    ]

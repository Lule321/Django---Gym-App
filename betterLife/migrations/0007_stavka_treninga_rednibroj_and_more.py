# Generated by Django 4.0.4 on 2022-05-29 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betterLife', '0006_alter_stavka_treninga_brojponavljanja'),
    ]

    operations = [
        migrations.AddField(
            model_name='stavka_treninga',
            name='redniBroj',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stavka_treninga',
            name='tezina',
            field=models.CharField(max_length=50),
        ),
    ]

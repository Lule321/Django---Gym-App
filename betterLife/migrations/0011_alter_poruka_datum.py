# Generated by Django 4.0.4 on 2022-05-31 10:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('betterLife', '0010_poruka_datum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poruka',
            name='datum',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
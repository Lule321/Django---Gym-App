# Generated by Django 4.0.4 on 2022-05-31 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betterLife', '0011_alter_poruka_datum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='razgovor',
            old_name='posaljilac',
            new_name='posiljalac',
        ),
    ]

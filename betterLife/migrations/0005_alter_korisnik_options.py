# Generated by Django 4.0.4 on 2022-05-23 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betterLife', '0004_alter_korisnik_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='korisnik',
            options={'permissions': (('trener', 'treneru omogucava njegove funkcionalnosti'),)},
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-11 00:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Korisnik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(max_length=1)),
                ('pfp', models.ImageField(null=True, upload_to='imgs/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Korisnik',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Jelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=30)),
                ('kalorije', models.IntegerField()),
                ('sastojci', models.CharField(max_length=256)),
                ('priprema', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'Jelo',
            },
        ),
        migrations.CreateModel(
            name='Pitanje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'db_table': 'Pitanje',
            },
        ),
        migrations.CreateModel(
            name='Plan_Ishrane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Plan_Ishrane',
            },
        ),
        migrations.CreateModel(
            name='Plan_Treninga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Plan_Treninga',
            },
        ),
        migrations.CreateModel(
            name='Sprava',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=30)),
                ('opis', models.CharField(max_length=256, null=True)),
                ('stanje', models.BooleanField(default=True)),
                ('datumNabavke', models.DateField()),
                ('kolicina', models.IntegerField()),
            ],
            options={
                'db_table': 'Sprava',
            },
        ),
        migrations.CreateModel(
            name='Trener',
            fields=[
                ('korisnik_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('radnoVreme', models.CharField(max_length=30, null=True)),
            ],
            options={
                'db_table': 'Trener',
            },
            bases=('betterLife.korisnik',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Vezba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=30)),
                ('opis', models.CharField(max_length=256, null=True)),
                ('tip', models.CharField(max_length=30, null=True)),
                ('misici', models.CharField(max_length=64)),
                ('sprava', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='betterLife.sprava')),
            ],
            options={
                'db_table': 'Vezba',
            },
        ),
        migrations.CreateModel(
            name='Trening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(max_length=30, null=True)),
                ('dan', models.DateField(null=True)),
                ('vreme', models.TimeField(null=True)),
                ('planTreninga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.plan_treninga')),
            ],
            options={
                'db_table': 'Trening',
            },
        ),
        migrations.CreateModel(
            name='Stavka_Treninga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brojPonavljanja', models.IntegerField()),
                ('tezina', models.IntegerField()),
                ('trening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.trening')),
                ('vezba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.vezba')),
            ],
            options={
                'db_table': 'Stavka_Treninga',
            },
        ),
        migrations.CreateModel(
            name='Stavka_Ishrane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.IntegerField()),
                ('dan', models.DateField()),
                ('vreme', models.TimeField()),
                ('jelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.jelo')),
                ('planIshrane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.plan_ishrane')),
            ],
            options={
                'db_table': 'Stavka_Ishrane',
            },
        ),
        migrations.CreateModel(
            name='Razgovor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posaljilac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posiljalac', to=settings.AUTH_USER_MODEL)),
                ('primalac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primalac', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poruka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redniBroj', models.IntegerField(default=1)),
                ('tekst', models.CharField(blank=True, max_length=256)),
                ('razgovor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.razgovor')),
            ],
            options={
                'db_table': 'Poruka',
            },
        ),
        migrations.CreateModel(
            name='Odgovor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(blank=True, max_length=256)),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pitanje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.pitanje')),
            ],
            options={
                'db_table': 'Odgovor',
            },
        ),
        migrations.CreateModel(
            name='Klijent',
            fields=[
                ('korisnik_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('brojClanskeKarte', models.IntegerField(unique=True)),
                ('pretplata', models.CharField(max_length=30)),
                ('visina', models.IntegerField(null=True)),
                ('tezina', models.IntegerField(null=True)),
                ('godine', models.IntegerField(null=True)),
                ('datumPoslednjeUplate', models.DateField(default=django.utils.timezone.now)),
                ('mojTrener', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betterLife.trener')),
            ],
            options={
                'db_table': 'Klijent',
            },
            bases=('betterLife.korisnik',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

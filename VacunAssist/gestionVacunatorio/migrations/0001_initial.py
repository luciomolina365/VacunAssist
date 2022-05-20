# Generated by Django 4.0.4 on 2022-05-20 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('dni', models.IntegerField(unique=True, verbose_name='Dni')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30, unique=True, verbose_name='Email')),
                ('dateOfBirth', models.DateField()),
                ('zone', models.CharField(choices=[('Terminal de ómnibus', 'Terminal de ómnibus'), ('Municipalidad de La Plata', 'Municipalidad de La Plata'), ('Cementerio', 'Cementerio')], max_length=30)),
                ('gender', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('secondFactor', models.IntegerField(blank=True, null=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Vaccinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('dni', models.IntegerField()),
                ('email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('timeSpan', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionVacunatorio.vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='Formulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk', models.BooleanField()),
                ('admissionDate', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AplicatedVaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doseNumber', models.IntegerField(blank=True, choices=[(1, 1), (2, 2)])),
                ('aplicationDate', models.DateField()),
                ('formulary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionVacunatorio.formulary')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionVacunatorio.vaccine')),
            ],
        ),
    ]

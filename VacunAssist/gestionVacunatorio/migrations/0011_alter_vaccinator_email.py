# Generated by Django 4.0.4 on 2022-06-09 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0010_remove_admin_dni_alter_vaccinator_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinator',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
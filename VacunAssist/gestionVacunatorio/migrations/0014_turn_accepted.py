# Generated by Django 4.0.4 on 2022-06-12 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0013_vaccinator_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]

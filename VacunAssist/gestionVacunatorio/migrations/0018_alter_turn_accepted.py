# Generated by Django 4.0.4 on 2022-06-27 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0017_remove_information_active_information_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='accepted',
            field=models.BooleanField(default=True),
        ),
    ]

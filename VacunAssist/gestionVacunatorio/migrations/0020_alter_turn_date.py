# Generated by Django 4.0.4 on 2022-07-02 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0019_turnrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='date',
            field=models.DateField(null=True),
        ),
    ]

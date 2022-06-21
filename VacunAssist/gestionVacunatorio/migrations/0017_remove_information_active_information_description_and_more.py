# Generated by Django 4.0.4 on 2022-06-21 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0016_information_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='active',
        ),
        migrations.AddField(
            model_name='information',
            name='description',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='information',
            name='email',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name='information',
            name='name',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name='information',
            name='tel',
            field=models.IntegerField(default=None),
        ),
    ]

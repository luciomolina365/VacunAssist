# Generated by Django 4.0.4 on 2022-05-20 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0005_alter_user_secondfactor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='user',
            name='dni',
            field=models.IntegerField(unique=True, verbose_name='Dni'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=30, unique=True, verbose_name='Email'),
        ),
    ]

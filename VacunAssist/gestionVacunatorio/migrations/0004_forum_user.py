# Generated by Django 4.0.4 on 2022-05-16 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVacunatorio', '0003_admin_aplicatedvaccine_formulary_forum_turn_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='user',
            field=models.CharField(default=2, max_length=30),
            preserve_default=False,
        ),
    ]

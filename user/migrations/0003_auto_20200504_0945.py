# Generated by Django 2.0 on 2020-05-04 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_mailcontrol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaluserprofile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile', verbose_name='Profil Fotoğrafı'),
        ),
    ]

# Generated by Django 2.0 on 2020-05-04 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200504_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaluserprofile',
            name='profile_photo',
            field=models.ImageField(blank=True, default=1, upload_to='peronaluser_profile', verbose_name='Profil Fotoğrafı'),
            preserve_default=False,
        ),
    ]
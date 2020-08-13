# Generated by Django 2.0 on 2020-05-15 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_auto_20200504_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalAwardSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_comment', models.IntegerField(verbose_name='Total Comment')),
                ('is_gold', models.BooleanField(default=False)),
                ('is_silver', models.BooleanField(default=False)),
                ('is_bronze', models.BooleanField(default=False)),
                ('positive_count', models.IntegerField(verbose_name='Total Positive')),
                ('negative_count', models.IntegerField(verbose_name='Total Negative')),
                ('notr_count', models.IntegerField(verbose_name='Total Notr')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
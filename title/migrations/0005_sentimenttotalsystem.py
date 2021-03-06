# Generated by Django 2.0 on 2020-05-15 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0004_auto_20200515_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentimentTotalSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive_count', models.IntegerField(verbose_name='Total Positive')),
                ('negative_count', models.IntegerField(verbose_name='Total Negative')),
                ('notr_count', models.IntegerField(verbose_name='Total Notr')),
                ('title', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='title.Title', verbose_name='Title')),
            ],
        ),
    ]

# Generated by Django 3.0.3 on 2020-03-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_speaker_wordpress_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speaker',
            name='wordpress_id',
        ),
        migrations.AddField(
            model_name='event',
            name='wordpress_url',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='speaker',
            name='wordpress_url',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]

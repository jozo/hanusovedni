# Generated by Django 2.2.9 on 2020-02-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_auto_20200207_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_url',
            field=models.URLField(blank=True, null=True, verbose_name='Lístok URL'),
        ),
    ]
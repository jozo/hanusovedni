# Generated by Django 2.1.8 on 2019-04-30 17:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_headersettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headersettings',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='headersettings',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

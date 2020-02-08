# Generated by Django 2.2.9 on 2020-01-27 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_remove_event_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.IllustrationImage'),
        ),
    ]
# Generated by Django 2.2.9 on 2020-02-21 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20200221_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heroimage',
            name='name',
        ),
    ]

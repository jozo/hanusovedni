# Generated by Django 3.0.4 on 2020-04-19 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0059_auto_20200419_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partnersection',
            name='page',
        ),
        migrations.DeleteModel(
            name='Partner2',
        ),
        migrations.DeleteModel(
            name='PartnerSection',
        ),
    ]
# Generated by Django 3.0.4 on 2020-04-09 21:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0045_auto_20200407_1833"),
    ]

    operations = [
        migrations.RenameField(
            model_name="menuitem",
            old_name="title",
            new_name="title_sk",
        ),
    ]

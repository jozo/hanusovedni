# Generated by Django 2.2.9 on 2020-02-24 20:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0019_auto_20200224_2132"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="show_on_frontpage",
            new_name="show_on_festivalpage",
        ),
    ]

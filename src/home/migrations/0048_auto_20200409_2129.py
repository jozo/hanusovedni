# Generated by Django 3.0.4 on 2020-04-09 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0047_menuitem_title_en"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="title_en",
            field=models.CharField(max_length=32),
        ),
    ]

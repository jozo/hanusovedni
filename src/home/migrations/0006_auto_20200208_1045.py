# Generated by Django 2.2.9 on 2020-02-08 09:45

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_festivalpage_formatted_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="festivalpage",
            name="formatted_title",
            field=wagtail.core.fields.RichTextField(default="", verbose_name="titulok"),
        ),
    ]

# Generated by Django 3.0.3 on 2020-03-19 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("home", "0034_auto_20200319_1358"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="related_festival",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.Page",
            ),
        ),
    ]

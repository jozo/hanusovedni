# Generated by Django 3.0.4 on 2020-05-09 23:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("home", "0084_auto_20200509_2244"),
    ]

    operations = [
        migrations.AlterField(
            model_name="opengraphimage",
            name="page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="open_graph_image",
                to="wagtailcore.Page",
            ),
        ),
    ]

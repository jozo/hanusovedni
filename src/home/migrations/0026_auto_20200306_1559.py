# Generated by Django 3.0.3 on 2020-03-06 14:59

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("home", "0025_auto_20200303_2253"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutFestivalPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.blocks.CharBlock(classname="title"),
                            ),
                            ("paragraph", wagtail.blocks.RichTextBlock()),
                        ]
                    ),
                ),
            ],
            options={
                "verbose_name": "o festivale",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.AlterModelOptions(
            name="contactpage",
            options={"verbose_name": "kontakt"},
        ),
    ]

# Generated by Django 3.0.3 on 2020-03-07 12:44

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0028_partnerspage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partnerspage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "partner",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("logo", wagtail.images.blocks.ImageChooserBlock()),
                                ("description", wagtail.core.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ]
            ),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-09 15:09

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models

import home.models.mixins


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("home", "0118_remove_contactpage_right_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketsPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "title_en",
                    models.CharField(
                        help_text="Názov stránky, ako by ste chceli, aby sa zobrazoval verejnosti",
                        max_length=255,
                        verbose_name="titulok",
                    ),
                ),
                (
                    "carousel_sk",
                    wagtail.fields.StreamField(
                        [
                            (
                                "item",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        ("url", wagtail.blocks.URLBlock()),
                                    ]
                                ),
                            )
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "carousel_en",
                    wagtail.fields.StreamField(
                        [
                            (
                                "item",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        ("url", wagtail.blocks.URLBlock()),
                                    ]
                                ),
                            )
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "body_sk",
                    wagtail.fields.StreamField(
                        [("text", wagtail.blocks.TextBlock())], use_json_field=True
                    ),
                ),
                (
                    "body_en",
                    wagtail.fields.StreamField(
                        [("text", wagtail.blocks.TextBlock())], use_json_field=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Tickets - created for BHD 2023",
            },
            bases=(home.models.mixins.FixUrlMixin, "wagtailcore.page"),
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-30 14:56

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0059_apply_collection_ordering"),
        ("home", "0098_streampage_popup_donation_button_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="PodcastPage",
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
                ("description_sk", wagtail.fields.RichTextField(blank=True)),
                ("description_en", wagtail.fields.RichTextField(blank=True)),
                (
                    "episodes",
                    wagtail.fields.StreamField(
                        [
                            (
                                "episode",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "number",
                                            wagtail.blocks.IntegerBlock(min_value=1),
                                        ),
                                        ("title_sk", wagtail.blocks.CharBlock()),
                                        ("title_en", wagtail.blocks.CharBlock()),
                                        (
                                            "category",
                                            wagtail.snippets.blocks.SnippetChooserBlock(
                                                "home.Category"
                                            ),
                                        ),
                                        ("url_anchor", wagtail.blocks.URLBlock()),
                                        ("url_apple", wagtail.blocks.URLBlock()),
                                        ("url_spotify", wagtail.blocks.URLBlock()),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]

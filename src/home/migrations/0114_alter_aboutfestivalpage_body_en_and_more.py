# Generated by Django 4.1.1 on 2022-09-21 07:48

from django.db import migrations
import home.models.data_models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0113_alter_event_buttons"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutfestivalpage",
            name="body_en",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(form_classname="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="aboutfestivalpage",
            name="body_sk",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(form_classname="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="crowdfundingpage",
            name="body_en",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.TextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="crowdfundingpage",
            name="body_sk",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.TextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="crowdfundingrocket2page",
            name="body_en",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.TextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="crowdfundingrocket2page",
            name="body_sk",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.TextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="crowdfundingstarspage",
            name="body_en",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.TextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="crowdfundingstarspage",
            name="body_sk",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.TextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="donatepage",
            name="body_en",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(form_classname="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="donatepage",
            name="body_sk",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(form_classname="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="buttons",
            field=wagtail.fields.StreamField(
                [
                    (
                        "button",
                        wagtail.blocks.StructBlock(
                            [
                                ("url", wagtail.blocks.URLBlock()),
                                ("color", wagtail.blocks.CharBlock(required=False)),
                                ("sk_text", wagtail.blocks.CharBlock()),
                                ("en_text", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                help_text="Tlačidlá len pre toto podujatie. Zobrazia sa vedla tlačidiel pre lístky.",
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="headline_en",
            field=wagtail.fields.StreamField(
                [
                    (
                        "headliner",
                        wagtail.blocks.StructBlock(
                            [
                                ("name", wagtail.blocks.CharBlock()),
                                ("photo", wagtail.images.blocks.ImageChooserBlock()),
                                ("link", wagtail.blocks.PageChooserBlock()),
                                ("description", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="headline_sk",
            field=wagtail.fields.StreamField(
                [
                    (
                        "headliner",
                        wagtail.blocks.StructBlock(
                            [
                                ("name", wagtail.blocks.CharBlock()),
                                ("photo", wagtail.images.blocks.ImageChooserBlock()),
                                ("link", wagtail.blocks.PageChooserBlock()),
                                ("description", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="hero_buttons_en",
            field=wagtail.fields.StreamField(
                [
                    (
                        "hero_buttons",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                ("link", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="hero_buttons_sk",
            field=wagtail.fields.StreamField(
                [
                    (
                        "hero_buttons",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                ("link", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="partner_sections",
            field=wagtail.fields.StreamField(
                [
                    (
                        "partner_section",
                        wagtail.blocks.StructBlock(
                            [
                                ("title_sk", wagtail.blocks.CharBlock()),
                                ("title_en", wagtail.blocks.CharBlock()),
                                (
                                    "partners",
                                    wagtail.blocks.ListBlock(
                                        home.models.data_models.PartnerBlock
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="partnerspage",
            name="body_en",
            field=wagtail.fields.StreamField(
                [
                    (
                        "partner",
                        wagtail.blocks.StructBlock(
                            [
                                ("logo", wagtail.images.blocks.ImageChooserBlock()),
                                ("description", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="partnerspage",
            name="body_sk",
            field=wagtail.fields.StreamField(
                [
                    (
                        "partner",
                        wagtail.blocks.StructBlock(
                            [
                                ("logo", wagtail.images.blocks.ImageChooserBlock()),
                                ("description", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="podcastpage",
            name="episodes",
            field=wagtail.fields.StreamField(
                [
                    (
                        "episode",
                        wagtail.blocks.StructBlock(
                            [
                                ("number", wagtail.blocks.IntegerBlock(min_value=1)),
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
                ],
                use_json_field=True,
            ),
        ),
    ]

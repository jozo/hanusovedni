# Generated by Django 4.1.8 on 2023-04-19 21:19

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0120_remove_event_ticket2_url_remove_event_ticket_url_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgramIndexPage2",
            fields=[
                (
                    "programindexpage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="home.programindexpage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("home.programindexpage",),
        ),
        migrations.AlterField(
            model_name="event",
            name="buttons",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "sk_text",
                                    wagtail.blocks.CharBlock(
                                        default="Kúp si vstupenku!"
                                    ),
                                ),
                                (
                                    "en_text",
                                    wagtail.blocks.CharBlock(default="Buy a ticket!"),
                                ),
                            ]
                        ),
                    ),
                    (
                        "button",
                        wagtail.blocks.StructBlock(
                            [
                                ("url", wagtail.blocks.URLBlock()),
                                ("color", wagtail.blocks.CharBlock()),
                                ("sk_text", wagtail.blocks.CharBlock()),
                                ("en_text", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                ],
                blank=True,
                help_text="Tlačidlá len pre toto podujatie. Zobrazia sa vedla tlačidiel pre lístky.",
                use_json_field=True,
            ),
        ),
        migrations.DeleteModel(
            name="HeroImage",
        ),
    ]

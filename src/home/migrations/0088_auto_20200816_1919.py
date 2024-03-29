# Generated by Django 3.1 on 2020-08-16 19:19

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0052_pagelogentry"),
        ("home", "0087_auto_20200515_1426"),
    ]

    operations = [
        migrations.CreateModel(
            name="Crowdfunding2Page",
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
                        blank=True,
                        help_text="Názov stránky, ako by ste chceli, aby sa zobrazoval verejnosti",
                        max_length=255,
                        verbose_name="titulok",
                    ),
                ),
                (
                    "body_sk",
                    wagtail.fields.StreamField([("text", wagtail.blocks.TextBlock())]),
                ),
                (
                    "body_en",
                    wagtail.fields.StreamField([("text", wagtail.blocks.TextBlock())]),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="formatted_title_en",
            field=wagtail.fields.RichTextField(
                default="",
                help_text="Visible in header next to the logo",
                verbose_name="titulok",
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="formatted_title_sk",
            field=wagtail.fields.RichTextField(
                default="",
                help_text="Visible in header next to the logo",
                verbose_name="titulok",
            ),
        ),
    ]

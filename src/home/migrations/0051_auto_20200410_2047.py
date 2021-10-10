# Generated by Django 3.0.4 on 2020-04-10 20:47

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0050_auto_20200410_1216"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutfestivalpage",
            name="body_en",
            field=wagtail.core.fields.StreamField(
                [
                    ("heading", wagtail.core.blocks.CharBlock(classname="title")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock()),
                ],
                default=None,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="title_en",
            field=models.CharField(default="", max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactpage",
            name="left_text_en",
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contactpage",
            name="right_text_en",
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="crowdfundingpage",
            name="body_en",
            field=wagtail.core.fields.StreamField(
                [("text", wagtail.core.blocks.TextBlock())], default=None
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="donatepage",
            name="body_en",
            field=wagtail.core.fields.StreamField(
                [
                    ("heading", wagtail.core.blocks.CharBlock(classname="title")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock()),
                ],
                default=None,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="description_en",
            field=wagtail.core.fields.RichTextField(blank=True, verbose_name="popis"),
        ),
        migrations.AddField(
            model_name="event",
            name="short_overview_en",
            field=models.CharField(
                blank=True,
                help_text="Zobrazuje sa na stránke s programom",
                max_length=255,
                verbose_name="krátky popis",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="title_en",
            field=models.CharField(default="", max_length=255, verbose_name="názov"),
        ),
        migrations.AddField(
            model_name="partnerspage",
            name="body_en",
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
                ],
                default=None,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="speaker",
            name="description_en",
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name="contactpage",
            name="left_text_sk",
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="contactpage",
            name="right_text_sk",
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]

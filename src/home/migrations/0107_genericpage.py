# Generated by Django 3.1.7 on 2021-09-07 18:46

import django.db.models.deletion
import wagtail.core.fields
from django.db import migrations, models

import home.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
        ("home", "0106_auto_20210617_0740"),
    ]

    operations = [
        migrations.CreateModel(
            name="GenericPage",
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
                ("body_sk", wagtail.core.fields.RichTextField()),
                ("body_en", wagtail.core.fields.RichTextField()),
            ],
            options={
                "abstract": False,
            },
            bases=(home.models.mixins.FixUrlMixin, "wagtailcore.page"),
        ),
    ]

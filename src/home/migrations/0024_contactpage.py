# Generated by Django 3.0.3 on 2020-03-03 19:52

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("wagtailimages", "0001_squashed_0021"),
        ("home", "0023_event_event_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactPage",
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
                ("left_text", wagtail.core.fields.RichTextField()),
                ("right_text", wagtail.core.fields.RichTextField()),
                (
                    "left_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.Image",
                    ),
                ),
                (
                    "right_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.Image",
                    ),
                ),
            ],
            options={"verbose_name": "kontakt", "verbose_name_plural": "kontakt",},
            bases=("wagtailcore.page",),
        ),
    ]

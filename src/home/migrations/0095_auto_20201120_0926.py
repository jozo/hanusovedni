# Generated by Django 3.1.3 on 2020-11-20 09:26

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0094_auto_20201119_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festivalpage',
            name='headline_en',
            field=wagtail.core.fields.StreamField([('headliner', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.PageChooserBlock()), ('description', wagtail.core.blocks.RichTextBlock())]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='festivalpage',
            name='headline_sk',
            field=wagtail.core.fields.StreamField([('headliner', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.PageChooserBlock()), ('description', wagtail.core.blocks.RichTextBlock())]))], blank=True, null=True),
        ),
    ]

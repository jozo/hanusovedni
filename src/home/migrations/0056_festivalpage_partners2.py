# Generated by Django 3.0.4 on 2020-04-18 18:44

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0055_auto_20200417_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='partners2',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('partner', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock()), ('logo', wagtail.images.blocks.ImageChooserBlock())]))], blank=True, null=True),
        ),
    ]
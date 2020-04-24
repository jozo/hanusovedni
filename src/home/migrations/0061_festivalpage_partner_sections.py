# Generated by Django 3.0.4 on 2020-04-19 08:41

from django.db import migrations
import home.models.data_models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0060_auto_20200419_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='partner_sections',
            field=wagtail.core.fields.StreamField([('partner_section', wagtail.core.blocks.StructBlock([('title_sk', wagtail.core.blocks.CharBlock()), ('title_en', wagtail.core.blocks.CharBlock()), ('partners', wagtail.core.blocks.ListBlock(home.models.data_models.PartnerBlock))]))], blank=True),
        ),
    ]
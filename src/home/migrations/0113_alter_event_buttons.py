# Generated by Django 3.2.8 on 2022-05-31 07:49

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0112_event_buttons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='buttons',
            field=wagtail.core.fields.StreamField([('button', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock()), ('color', wagtail.core.blocks.CharBlock(required=False)), ('sk_text', wagtail.core.blocks.CharBlock()), ('en_text', wagtail.core.blocks.CharBlock())]))], blank=True, help_text='Tlačidlá len pre toto podujatie. Zobrazia sa vedla tlačidiel pre lístky.'),
        ),
    ]
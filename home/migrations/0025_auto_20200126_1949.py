# Generated by Django 2.2.9 on 2020-01-26 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_event_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='video_url',
            field=models.URLField(blank=True, help_text="Podporuje Youtube, Vimeo a <a href='https://github.com/wagtail/wagtail/blob/master/wagtail/embeds/oembed_providers.py' target='_blank'>dalšie stránky</a>", null=True),
        ),
    ]
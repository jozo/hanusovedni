# Generated by Django 3.0.4 on 2020-03-20 20:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("home", "0038_auto_20200320_1135"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SupportPage",
            new_name="DonatePage",
        ),
    ]

# Generated by Django 2.2.9 on 2020-02-07 12:38

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_auto_20200207_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='title',
            field=wagtail.core.fields.RichTextField(blank=True, verbose_name='názov'),
        ),
    ]

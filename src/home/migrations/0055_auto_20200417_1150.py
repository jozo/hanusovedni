# Generated by Django 3.0.4 on 2020-04-17 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0054_event_title_en"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventindexpage",
            name="intro",
        ),
        migrations.RemoveField(
            model_name="programindexpage",
            name="intro",
        ),
        migrations.AddField(
            model_name="aboutfestivalpage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="contactpage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="crowdfundingpage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="donatepage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="eventindexpage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="partnerspage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="programindexpage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
        migrations.AddField(
            model_name="speakerindexpage",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Titulok stránky ktorý budú vidieť ostatní návštevníci",
                max_length=255,
                verbose_name="titulok",
            ),
        ),
    ]

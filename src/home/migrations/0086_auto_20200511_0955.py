# Generated by Django 3.0.4 on 2020-05-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("wagtailimages", "0001_squashed_0021"),
        ("home", "0085_auto_20200509_2300"),
    ]

    operations = [
        migrations.AddField(
            model_name="opengraphimage",
            name="lang_code",
            field=models.CharField(default="sk", max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name="opengraphimage", unique_together={("page", "image", "lang_code")},
        ),
    ]

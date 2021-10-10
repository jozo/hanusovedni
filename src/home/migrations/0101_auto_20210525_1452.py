# Generated by Django 3.1.7 on 2021-05-25 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0100_auto_20210525_0848"),
    ]

    operations = [
        migrations.AlterField(
            model_name="speakerconnection",
            name="speaker",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="speaker_connections",
                to="home.speaker",
            ),
        ),
    ]

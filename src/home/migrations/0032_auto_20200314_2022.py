# Generated by Django 3.0.3 on 2020-03-14 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0031_auto_20200307_1549"),
    ]

    operations = [
        migrations.AlterField(
            model_name="speaker",
            name="first_name",
            field=models.CharField(blank=True, max_length=64, verbose_name="meno"),
        ),
        migrations.AlterField(
            model_name="speaker",
            name="last_name",
            field=models.CharField(max_length=64, verbose_name="priezvisko"),
        ),
    ]

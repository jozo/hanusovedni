# Generated by Django 3.1.7 on 2021-05-29 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0103_crowdfundingcandlepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='crowdfundingcandlepage',
            name='feed_url',
            field=models.URLField(blank=True, help_text='URL from darujme.sk with donation amount'),
        ),
    ]
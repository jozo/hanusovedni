# Generated by Django 3.0.4 on 2020-04-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_auto_20200409_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='title_en',
            field=models.CharField(default='', max_length=32, verbose_name='titulok'),
            preserve_default=False,
        ),
    ]
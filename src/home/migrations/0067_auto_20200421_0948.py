# Generated by Django 3.0.4 on 2020-04-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0066_auto_20200421_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streampage',
            name='button_text_en',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='streampage',
            name='button_text_sk',
            field=models.CharField(max_length=100),
        ),
    ]
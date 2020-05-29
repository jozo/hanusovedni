# Generated by Django 3.0.4 on 2020-05-15 14:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0086_auto_20200511_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('event', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_connections', to='home.Event')),
                ('speaker', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='host_connections', to='home.Speaker')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ModeratorConnection',
        ),
    ]
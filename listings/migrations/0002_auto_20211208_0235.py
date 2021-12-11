# Generated by Django 3.2 on 2021-12-08 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='reserved_from',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='reserved_to',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
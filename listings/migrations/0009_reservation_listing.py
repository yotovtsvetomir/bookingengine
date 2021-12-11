# Generated by Django 3.2 on 2021-12-08 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_auto_20211208_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='listings.listing'),
        ),
    ]

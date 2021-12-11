# Generated by Django 3.2 on 2021-12-08 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0012_rename_apartment_reservation_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='hotel_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='listings.hotelroom'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='listings.listing'),
        ),
    ]
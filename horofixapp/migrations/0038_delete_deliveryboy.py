# Generated by Django 4.2.7 on 2023-11-26 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0037_remove_deliveryboy_emergency_contact_number_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeliveryBoy',
        ),
    ]
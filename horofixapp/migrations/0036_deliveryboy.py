# Generated by Django 4.2.7 on 2023-11-22 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0035_delete_deliveryboy'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryBoy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_proof_number', models.CharField(max_length=20)),
                ('qualification', models.CharField(max_length=50)),
                ('emergency_contact_number', models.CharField(max_length=15)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
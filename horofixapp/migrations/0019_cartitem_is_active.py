# Generated by Django 4.2.5 on 2023-11-06 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0018_order_orderitem_order_products_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]